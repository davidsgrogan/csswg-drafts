This document describes the accessibility of the proposed HTML elements `<menubar>`, `<menulist>`, and `<menuitem>`, along with attributes such as `checkable` and `defaultchecked`. (Note that the `command` and `commandfor` attributes are relatively new, but preexisting, HTML attributes). These elements and attributes are intended to provide native semantics that map directly to ARIA roles and states.

# Rules

1. `MENUBAR` elements have role [`menubar`](https://w3c.github.io/aria/#menubar).
2. `MENULIST` elements have role [`menu`](https://w3c.github.io/aria/#menu).
3. `MENUITEM` elements *usually* have role [`menuitem`](https://w3c.github.io/aria/#menuitem).
4. `MENUITEM`s can have `menuitemradio` or `menuitemcheckbox` roles depending on the checkable attribute of a parent fieldset
    1. `menuitemradio` and `menuitemcheckbox` elements have the `checked` attribute if they are checked
5. `menuitem`s and `button`s that are submenu invokers have `expanded=True` or `expanded=False` state but will NOT get an aria-details pointing to the popover -- https://github.com/openui/open-ui/issues/1297#issuecomment-3376865931
8. `button`s and `menuitem`s that are  `menu` invokers [have `haspopup=menu`](https://github.com/openui/open-ui/issues/1297#issuecomment-3376865931)
6. `menubar` and `menu` have `setSize`
7. `menuitem` descendants of a `menubar` or `menu` have `setSize` and `posInSet`
9. `menuitem`, `menuitemcheckbox`, `menuitemradio` are included in the accessibility tree even when they are disabled
10. An invoked `menulist` implicitly derives its accessible name from its invoker. The browser computes this in the accessibility tree exactly like `aria-labelledby` (without adding actual DOM attributes) unless an explicit `aria-labelledby` already exists.

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
    <menuitem disabled defaultchecked>Radio 2</menuitem>
    <menuitem>Radio 3</menuitem>
  </fieldset>
</menulist>
```

## Everything closed

At first, when nothing is clicked or activated, we have

<img src="file-view-closed.png" width="161">

```h
menubar setSize=2
  menuitem name="File" expanded=False haspopup=menu setSize=2 posInSet=1
  menuitem name="View" expanded=False haspopup=menu setSize=2 posInSet=2
```

## File activated

When you click/activate the File menu, the tree changes to:

<img src="file-open.png" width="188">

 ```h
 menubar setSize=2
  menuitem name="File" expanded=True haspopup=menu setSize=2 posInSet=1
  menuitem name="View" expanded=False haspopup=menu setSize=2 posInSet=2
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

<img src="view-open1.png" width="233">

```h
menubar setSize=2
  menuitem name="File" expanded=False haspopup=menu setSize=2 posInSet=1
  menuitem name="View" expanded=True haspopup=menu setSize=2 posInSet=2
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

<img src="button-labelledby.png" width="100">

```html
<button id="btn" commandfor="menu" command="show-menu">Open Menu</button>
<menulist id="menu">
  <menuitem>Item 1</menuitem>
</menulist>
```

```c
button name="Open Menu" expanded=True haspopup=menu
menu name="Open Menu" setSize=1
  menuitem name="Item 1" setSize=1 posInSet=1
```

 TODO:
  * Ask open questions with what we have left, including my draft local CL
  * Animated gif of Example 1?
