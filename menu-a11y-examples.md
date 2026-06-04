This DRAFT document describes a potential accessibility approach to the [proposed HTML elements `<menubar>`, `<menulist>`, and `<menuitem>`](https://open-ui.org/components/menu.explainer), and attributes `checkable` and `defaultchecked`. (Note that the [`command` and `commandfor` attributes](https://developer.mozilla.org/en-US/docs/Web/API/HTMLButtonElement/command) are preexisting, though relatively new, HTML attributes). These elements and attributes are intended to provide native semantics that map to existing ARIA roles and states.

# Rules

1. `<menubar>` elements have role [`menubar`](https://w3c.github.io/aria/#menubar).
2. `<menulist>` elements have role [`menu`](https://w3c.github.io/aria/#menu).
3. `<menuitem>` elements *usually* have role [`menuitem`](https://w3c.github.io/aria/#menuitem).
4. `<menuitem>`s can have [`menuitemradio`](https://w3c.github.io/aria/#menuitemradio) or [`menuitemcheckbox`](https://w3c.github.io/aria/#menuitemcheckbox) roles depending on the checkable attribute of a parent fieldset
    1. `menuitemradio` and `menuitemcheckbox` elements expose a boolean `checked` state
5. `menuitem`s and `button`s that are `menu` invokers
   1. have `expanded=true` or `expanded=false` state
   3. have `haspopup=menu`
   2. will NOT have `details` pointing to the `menu`
   4. [past discussion of these points](https://github.com/openui/open-ui/issues/1297#issuecomment-3376865931)
6. `menubar` and `menu` have `setSize`
7. `menuitem` descendants of a `menubar` or `menu` have `setSize` and `posInSet`
8. `menuitem`, `menuitemcheckbox`, `menuitemradio` are included in the accessibility tree even when they are disabled
9. An invoked `menulist` implicitly derives its accessible name from its invoker. The browser computes this in the accessibility tree exactly like `aria-labelledby` (*without* adding actual DOM attributes) unless an explicit `aria-labelledby` already exists.

# Example 1 -- File menu

First example is a small version of the menubar that adorns the top of many applications.
This one has only File and View. The HTML:

```html
<menubar>
  <menuitem commandfor="file-menu" command="toggle-menu">File</menuitem>
  <menuitem commandfor="view-menu" command="toggle-menu">View</menuitem>
</menubar>

<menulist id="file-menu">
  <menuitem>New</menuitem>
  <hr>
  <menuitem>Save</menuitem>
  <menuitem>Save As...</menuitem>
  <menuitem disabled>Print</menuitem>
  <hr>
  <menuitem>Exit</menuitem>
</menulist>

<menulist id="view-menu">
  <fieldset checkable="multiple">
    <menuitem disabled>Checkbox 1</menuitem>
    <menuitem disabled defaultchecked>Checkbox 2</menuitem>
    <menuitem>Checkbox 3</menuitem>
  </fieldset>
  <fieldset checkable="single">
    <menuitem disabled>Radio 1</menuitem>
    <menuitem defaultchecked>Radio 2</menuitem>
  </fieldset>
</menulist>
```

## Everything closed

At first, when nothing is clicked or activated, we have

<img src="file-view-closed.png" width="161" alt="Screenshot of a menubar with File and View items, both closed.">

```ruby
menubar setSize=2
    menuitem name="File" expanded=false haspopup=menu setSize=2 posInSet=1
    menuitem name="View" expanded=false haspopup=menu setSize=2 posInSet=2
```

## File activated

When you click/activate the File menu, the tree changes to:

<img src="file-open.png" width="188" alt="Screenshot of the menubar with the File menu opened, showing a dropdown with New, Save, Save As..., Print (disabled), and Exit.">

```ruby
menubar setSize=2
    menuitem name="File" expanded=true haspopup=menu setSize=2 posInSet=1
    menuitem name="View" expanded=false haspopup=menu setSize=2 posInSet=2
menu name="File" setSize=5
    menuitem name="New" setSize=5 posInSet=1
    separator
    menuitem name="Save" setSize=5 posInSet=2
    menuitem name="Save As..." setSize=5 posInSet=3
    menuitem name="Print" disabled setSize=5 posInSet=4
    separator
    menuitem name="Exit" setSize=5 posInSet=5
```

## View activated

<img src="view-open1.png" width="233" alt="Screenshot of the menubar with the View menu opened. The dropdown shows disabled unchecked Checkbox 1, disabled checked Checkbox 2, enabled unchecked Checkbox 3, disabled unchecked Radio 1, and enabled checked Radio 2.">

```ruby
menubar setSize=2
    menuitem name="File" expanded=false haspopup=menu setSize=2 posInSet=1
    menuitem name="View" expanded=true haspopup=menu setSize=2 posInSet=2
menu name="View" setSize=5
    group
        menuitemcheckbox name="Checkbox 1" disabled checked=false setSize=3 posInSet=1
        menuitemcheckbox name="Checkbox 2" disabled checked=true setSize=3 posInSet=2
        menuitemcheckbox name="Checkbox 3" checked=false setSize=3 posInSet=3
    group
        menuitemradio name="Radio 1" disabled checked=false setSize=2 posInSet=1
        menuitemradio name="Radio 2" checked=true setSize=2 posInSet=2
```

# Example 2 -- menu labelledby the opener

<img src="button-labelledby.png" width="100" alt="Screenshot of an 'Open Menu' button with a dropdown menu open below it showing 'Item 1'.">

```html
<button id="btn" commandfor="menu" command="show-menu">Open Menu</button>
<menulist id="menu">
  <menuitem>Item 1</menuitem>
</menulist>
```

```ruby
button name="Open Menu" expanded=true haspopup=menu
menu name="Open Menu" setSize=1
    menuitem name="Item 1" setSize=1 posInSet=1
```

## Related Open Questions
1. [How do we achieve soft disabling of menu items?](https://github.com/openui/open-ui/issues/1274)
2. [What should the content model be and what exactly do we do when it is violated?](https://github.com/openui/open-ui/issues/1433)

## Related links
1. [Minutes and slideshow from TPAC 2025 when Dom Farolino initially presented menu elements to ARIA](https://github.com/w3c/aria/issues/2658#issuecomment-3947872243)
