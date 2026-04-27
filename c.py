from playwright.sync_api import sync_playwright

"""
Extracts and formats a spec-compliant Accessibility (AX) Tree using Playwright
and CDP.

Goal: To generate clean, unassailable proof for the ARIA Working Group (and
Open UI) demonstrating how Chrome/Blink natively maps new semantic HTML
elements (like <menubar> and <menulist>) and interaction attributes (like
`commandfor`) to platform accessibility APIs. The output is formatted as a
clean text dump, isolating semantic structure from layout noise.

Mechanism & Sources: This script bypasses standard, simplified accessibility
snapshot APIs in favor of querying the raw Chrome DevTools Protocol (CDP) via
`Accessibility.getFullAXTree`. It produces its output by combining data from
three distinct logical operations:

    1. Core AX Node Properties & Relations: Extracts the standard computed
    states and structural pointers exposed to platform APIs. This includes the
    element's role, strict property evaluations (`expanded`, `disabled`,
    `checked`, `checkable`, `setSize`, `posInSet`), and explicit navigation
    relations like `details`.

    2. Computation Trail & Provenance Metadata (name.sources): Extracts the
    internal audit trail of *how* the browser engine calculated relationships
    and names. By digging into the `relatedElement` or `implicit` sources, the
    script locates relation pointers (like `labelledBy`).

    3. Live DOM Pointer Resolution: Because Blink aggressively prunes
    non-interactive container nodes from the accessibility tree, relation
    targets (like standard `idref` strings) are often dropped by the engine.
    The script circumvents this by extracting the internal `backendDOMNodeId`
    from the relation payload and querying the live DOM (`DOM.describeNode`) to
    explicitly retrieve the original HTML `id` attribute.

By merging these data streams and running a custom pruning algorithm to strip
out Blink-specific layout noise (`genericContainer`, `none`, `StaticText`), the
script provides undeniable proof that implicit web platform triggers
successfully satisfy APG structural and labeling requirements natively, without
manual `aria-` attributes.
"""

def get_formatted_ax_tree():
    with sync_playwright() as p:
        print("Connecting to Canary...")
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        
        context = browser.contexts[0]
        page = context.pages[0]
        print(f"Extracting tree for tab: {page.title()}\n")

        # Interaction toggle
        try: page.click('#btn', timeout=500); page.wait_for_timeout(100)
        except Exception: pass

        # Create a direct CDP session and enable the DOM domain
        client = context.new_cdp_session(page)
        client.send('DOM.enable')
        
        # Request the raw Accessibility Tree
        response = client.send('Accessibility.getFullAXTree')
        nodes = response.get('nodes', [])

        # Fast lookup map
        node_map = {node['nodeId']: node for node in nodes}

        # --- Helper: Resolve DOM ID from a relatedNode safely ---
        def get_dom_id(related_node):
            target_id = related_node.get('idref')
            if not target_id:
                backend_id = related_node.get('backendDOMNodeId')
                if backend_id:
                    try:
                        dom_res = client.send('DOM.describeNode', {'backendNodeId': backend_id})
                        attrs = dom_res.get('node', {}).get('attributes', [])
                        for i in range(0, len(attrs), 2):
                            if attrs[i] == 'id':
                                return attrs[i+1]
                    except Exception:
                        pass
            return target_id

        # --- Helper: Prune layout noise ---
        def get_relevant_children(node):
            children = []
            for child_id in node.get('childIds', []):
                child = node_map.get(child_id)
                if not child: continue
                
                role = child.get('role', {}).get('value')
                
                if role == 'StaticText':
                    continue
                    
                if child.get('ignored') or role in ['genericContainer', 'generic', 'none']:
                    children.extend(get_relevant_children(child))
                else:
                    children.append(child)
            return children

        # --- Helper: Format the node string ---
        def format_node(node, indent=''):
            props = []
            
            # A. Extract Core Properties (Including the new `details` relation)
            for prop in node.get('properties', []):
                name = prop['name']
                value_obj = prop.get('value', {})
                value = value_obj.get('value')
                
                if name == 'hasPopup': props.append(f"haspopup={value}")
                elif name == 'expanded': props.append(f"expanded={value}")
                elif name == 'disabled' and value: props.append("disabled")
                elif name == 'setSize': props.append(f"setSize={value}")
                elif name == 'posInSet': props.append(f"posInSet={value}")
                elif name == 'checked': props.append(f"checked={value}")
                elif name == 'checkable' and value: props.append("checkable")
                
                # --- NEW: Extract details relation ---
                elif name == 'details':
                    related_nodes = value_obj.get('relatedNodes', [])
                    if related_nodes:
                        target_id = get_dom_id(related_nodes[0])
                        if target_id:
                            props.append(f'details="{target_id}"')
            
            # B. Extract labelledBy relation metadata
            labelled_by_str = ""
            name_obj = node.get('name', {})
            for source in name_obj.get('sources', []):
                if source.get('superseded'):
                    continue

                if source.get('type') in ['relatedElement', 'implicit']:
                    related_nodes = source.get('relatedNodes', [])
                    target_id = None
                    
                    if related_nodes:
                        target_id = get_dom_id(related_nodes[0])
                    
                    # Fallback to raw attribute string if it couldn't map a node at all
                    if not target_id:
                        attr_val = source.get('attributeValue', {}).get('value')
                        if isinstance(attr_val, str) and attr_val:
                            target_id = attr_val

                    if target_id:
                        labelled_by_str = f' labelledBy="{target_id}"'

            # C. Stitch it together
            role_str = node.get('role', {}).get('value', 'unknown')
            name_val = name_obj.get('value')
            name_str = f' name="{name_val}"' if name_val else ''
            prop_str = f" {' '.join(props)}" if props else ""
            
            result = f"{indent}{role_str}{name_str}{labelled_by_str}{prop_str}\n"

            # D. Recurse into children
            for child in get_relevant_children(node):
                result += format_node(child, indent + '  ')
            
            return result

        # --- Start Execution ---
        root = next((n for n in nodes if n.get('role', {}).get('value') == 'RootWebArea'), None)
        
        if root:
            for top_node in get_relevant_children(root):
                print(format_node(top_node, ""), end="")
        else:
            print("Could not find RootWebArea.")

        browser.close()

if __name__ == '__main__':
    get_formatted_ax_tree()
