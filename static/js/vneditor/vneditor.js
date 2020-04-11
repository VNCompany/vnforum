jQuery.fn.extend({
    insertAtCursor: function (myValue) {
        return this.each(function (i) {
            if (document.selection) {
                this.focus();
                sel = document.selection.createRange();
                sel.text = myValue;
                this.focus();
            } else if (this.selectionStart || this.selectionStart == "0") {
                var startPos = this.selectionStart;
                var endPos = this.selectionEnd;
                var scrollTop = this.scrollTop;
                this.value = this.value.substring(0, startPos) + myValue + this.value.substring(endPos, this.value.length);
                this.focus();
                this.selectionStart = startPos + myValue.length;
                this.selectionEnd = startPos + myValue.length;
                this.scrollTop = scrollTop;
            } else {
                this.value += myValue;
                this.focus();
            }
        });
    },
    insertAroundCursor: function (myValueBefore, myValueAfter) {
        return this.each(function (i) {
            if (document.selection) {
                this.focus();
                sel = document.selection.createRange();
                sel.text = myValueBefore + sel.text + myValueAfter;
                this.focus();
            } else if (this.selectionStart || this.selectionStart == "0") {
                var startPos = this.selectionStart;
                var endPos = this.selectionEnd;
                var scrollTop = this.scrollTop;
                this.value = this.value.substring(0, startPos) + myValueBefore + this.value.substring(startPos, endPos) + myValueAfter + this.value.substring(endPos, this.value.length);
                this.focus();
                this.selectionStart = startPos + myValueBefore.length;
                this.selectionEnd = endPos + myValueBefore.length;
                this.scrollTop = scrollTop;
            } else {
                this.value += myValueBefore + myValueAfter;
                this.focus();
            }
        });
    },
    selectRange: function (start, end) {
        return this.each(function (i) {
            if (this.setSelectionRange) {
                this.focus();
                this.setSelectionRange(start, end);
            } else if (this.createTextRange) {
                var range = this.createTextRange();
                range.collapse(true);
                range.moveEnd('character', end);
                range.moveStart('character', start);
                range.select();
            }
        });
    }
});

lib = '<div class="vne-body">\
<div class="control-panel">\
    <button type="button" data-action="[B]|[/B]" class="vne-head-btn vne-btn-bold">B</button>\
    <button type="button" data-action="[I]|[/I]" class="vne-head-btn vne-btn-italic">I</button>\
    <button type="button" data-action="[U]|[/U]" class="vne-head-btn vne-btn-underline">U</button>\
    <button type="button" data-action="[IMG=`|`]" class="vne-head-btn">IMG</button>\
    <button type="button" data-action="[LINK=``]|[/LINK]" class="vne-head-btn vne-btn-link">LINK</button>\
    <button type="button" data-action="[QUOTE]|[/QUOTE]" class="vne-head-btn">QUOTE</button>\
</div>\
<div class="control-panel code-panel">\
    <button type="button" data-action="[CODE=`html`]|[/CODE]" class="vne-head-btn">HTML</button>\
    <button type="button" data-action="[CODE=`css`]|[/CODE]" class="vne-head-btn">CSS</button>\
    <button type="button" data-action="[CODE=`csharp`]|[/CODE]" class="vne-head-btn">C#</button>\
    <button type="button" data-action="[CODE=`javascript`]|[/CODE]" class="vne-head-btn">JAVASCRIPT</button>\
    <button type="button" data-action="[CODE=`python`]|[/CODE]" class="vne-head-btn">PYTHON</button>\
    <button type="button" data-action="[CODE=`php`]|[/CODE]" class="vne-head-btn">PHP</button>\
</div>\
<div class="vne-ta">\
    <textarea {args} id="{0}" name="{1}" class="vne-ta-self"></textarea>\
</div>\
</div>';

let s;

VNE = {
    init: function (obj) {
        let id = "id" in obj ? obj.id : "content";
        let name = "name" in obj ? obj.name : "content";
        if ("selector" in obj) {
            let selector = obj.selector;
            let attrs = "attrs" in obj ? obj.attrs : "";
            let ss = undefined;
            if ("content_selector" in obj) {
                ss = $(obj.content_selector);
            }
            $(selector).html(
                lib.replace("{args}", attrs)
                    .replace("{0}", id)
                    .replace("{1}", name)
            );
            s = "#" + id;
            if (ss !== undefined) {
                $(s).html(ss.html());
            }
        }
    },

    css: function (styles) {
        $(".vne-body").css(styles);
    },

    appendAfter: function (text) {
        let element = $(s);
        element.html(text + element.html());
    },

    appendBefore: function (text) {
        let element = $(s);
        element.html(element.html() + text);
    },

    setText: function (text) {
        let element = $(s);
        element.html(text);
    }
};

$(document).ready(function () {
    $(".vne-head-btn").click(function (e) {
        let value = $(e.target).attr("data-action").replace(/`/g, '"').split("|");
        $(s).insertAroundCursor(value[0], value[1]);
    });
});
