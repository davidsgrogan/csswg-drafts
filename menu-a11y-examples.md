Basic

<img src="Screenshot%202026-03-03%20at%2011.33.17%E2%80%AFAM.png" width="200">

```html
<menubar>
  <menuitem commandfor="file-menu" command="toggle-menu">File</menuitem>
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
```

 * The `MENUBAR` has role [`menubar`](https://w3c.github.io/aria/#menubar).
 * The `MENULIST` has role [`menu`](https://w3c.github.io/aria/#menu).
* Each `MENUITEM` has role [`menuitem`](https://w3c.github.io/aria/#menuitem).
 * When you click/activate the File menu, we implicitly add the state

```
rootWebArea htmlTag='#document'
++genericContainer
++++genericContainer htmlTag='body'
++++++menuBar htmlTag='menubar'
++++++++menuItem htmlTag='menuitem' name='File' nameFrom=contents
++++++++++staticText name='File' nameFrom=contents
++++++++++++inlineTextBox name='File' nameFrom=contents
++++++menu
```

Things we do in menus
 * expanded state when the popover is open 8313111a56f54
 * setSize on menuBar fa5fee49e9622e8c45
 * setSize and posInSet on menuItem when they are in a menubar
 * checkable of the parent fieldset determines kMenuItemCheckBox and kMenuItemRadio
   * Also checked state for these elements 28856bebd73c680e7870
 * menuitem, menuitemcheckbox, menuitemradio are included in axtree even when they are disabled 94972a7ddb938c
 * When a MENULIST is invoked via `commandfor`, it gets aria-labelledby its invoker 41af4c311dec1e5ddb93

 TODO:
  * Figure out examples for those. Crib from the tests for each CL.
  * Use c.py to extract trees. HOPEFULLY is finished, but fire up gcli to make more changes if necessary.
  * This ^^ will take ~ 1 hour.
  * Ask open questions with what we have left, including my draft local CL
  * Make a master example with bunch of stuff and animated gif showing it in action
