
from __future__ import annotations
import gradio as gr
import pytermgui as ptg

from modules.ui_components import ( ResizeHandleRow, FormRow, FormColumn, InputAccordion,
        FormGroup, ToolButton,
)


def makeSlider(component: gr.Slider) -> ptg.Splitter:
    slider = ptg.Splitter(
        ptg.Splitter(component.label),
        ptg.Slider(),
        ptg.Splitter(str(component.value))
    )
    return slider

def makeNumber(component: gr.Number) -> ptg.Splitter:
    number = ptg.Splitter(
        ptg.Splitter(component.label),
        ptg.InputField(str(component.value)),
    )
    return number

def makeTextbox(component: gr.Textbox) -> ptg.Splitter:
    textbox = ptg.Splitter(
        ptg.Splitter(component.label),
        ptg.InputField(str(component.value)),
    )
    return textbox

def makeButton(component: gr.Button) -> ptg.Button:
    return ptg.Button(component.label, lambda *_: None)

def makeColumn(component) -> ptg.Container:
    list = convertGradioIntoPytuiList(component)
    if len(list) == 0:
        return None
    col = ptg.Container(*list)
    return col

def makeRow(component) -> ptg.Splitter:
    list = convertGradioIntoPytuiList(component)
    if len(list) == 0:
        return None
    return ptg.Splitter(*list)

def makeCheckbox(component: gr.Checkbox) -> ptg.Splitter:
    checkbox = ptg.Splitter(
        ptg.Splitter(component.label),
        ptg.Checkbox(lambda *_: None, component.value)
    )
    return checkbox

def makeAccordion(component: gr.Accordion) -> ptg.Collapsible:
    return ptg.Collapsible(component.label, *convertGradioIntoPytuiList(component))

def makeInputAccordion(component: InputAccordion) -> ptg.Collapsible:
    checkbox = ptg.Splitter(
        ptg.Splitter('enable'),
        ptg.Checkbox(lambda *_: None, component.value)
    )
    inputAccordion = ptg.Collapsible(
        component.label,
        checkbox,
        *convertGradioIntoPytuiList(component.accordion)
    )
    return inputAccordion

def makeDropdown(component: gr.Dropdown) -> ptg.Button:
    return ptg.Button(component.label, lambda *_: None)


forbiddenLabels = ['Hires. fix', 'Refiner']

def convertGradioIntoPytuiList(blocks) -> list:
    entry = []
    for component in getattr(blocks, 'children', []):
        try:
            if not getattr(component, 'visible', False):
                continue
            if getattr(component, 'label', None) in forbiddenLabels:
                continue

            if type(component) is gr.Slider:
                entry.append(makeSlider(component))

            elif type(component) is gr.Number:
                entry.append(makeNumber(component))

            elif type(component) is gr.Textbox:
                entry.append(makeTextbox(component))

            elif type(component) is gr.Button:
                entry.append(makeButton(component))

            elif type(component) in (FormColumn, gr.Column):
                col = makeColumn(component)
                if col is not None:
                    entry.append(col)

            elif type(component) in (ResizeHandleRow, FormRow, gr.Row):
                row = makeRow(component)
                if row is not None:
                    entry.append(row)

            elif type(component) is gr.Checkbox:
                entry.append(makeCheckbox(component))
            
            elif type(component) is gr.Accordion:
                entry.append(makeAccordion(component))
            
            elif type(component) is InputAccordion:
                entry.append(makeInputAccordion(component))

            elif type(component) is gr.Dropdown:
                entry.append(makeDropdown(component))
            
            # add gr.Radio gr.CheckpointGroup

            elif type(component) in (gr.layouts.Form, gr.Group, gr.Blocks, FormGroup):
                entry.extend(convertGradioIntoPytuiList(component))

            else:
                print(f'unknown component: {type(component)}')
        except Exception as e:
            print(f'*** error while making: "{type(component)}" -', e)

    return entry


def findElementById(component, elem_id):
    for child in getattr(component, 'children', []):
        if getattr(child, 'elem_id', None) == elem_id:
            return child
        found = findElementById(child, elem_id)
        if found:
            return found
    return None
