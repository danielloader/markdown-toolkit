from markdown_toolkit import MarkdownDocument, bold


def test_document_render():
    with open("tests/test_document_render.md", "r", encoding="UTF-8") as file:
        doc = MarkdownDocument()
        with doc.heading("Title"):
            with doc.list:
                doc.unordered_item(doc.heading("List Subtitle"))
                doc.paragraph(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer ac odio euismod, sodales ipsum id, scelerisque nisl. Etiam erat odio, faucibus ut augue nec, tristique imperdiet ligula. Sed lacinia massa sed ante facilisis, eu finibus arcu fermentum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Morbi commodo, urna sit amet gravida luctus, nunc mauris aliquam orci, non laoreet lectus nulla sed mi. Nulla consectetur et tortor vel lacinia. Donec hendrerit condimentum ante id aliquet. Aenean condimentum nisl at ultrices ultricies. Donec ullamcorper nisl quis consectetur accumsan. Fusce posuere velit a augue bibendum tincidunt. Nullam suscipit turpis velit. Aenean a porttitor lorem. In sodales turpis in placerat egestas. Phasellus eros lectus, pharetra non augue at, vestibulum feugiat dolor."
                )
                doc.paragraph(
                    "Interdum et malesuada fames ac ante ipsum primis in faucibus. Etiam luctus mollis lacus ac luctus. Praesent justo mauris, lacinia ut neque vel, semper viverra ipsum. Nulla facilisi. Proin gravida augue eget blandit tincidunt. Nullam viverra iaculis semper. Nam quis turpis varius, euismod dui ac, rhoncus orci."
                )
            with doc.list:
                doc.unordered_item(doc.heading("List Subtitle"))
                doc.paragraph(
                    "Example of a paragraph explaining a nested ordered list below."
                )
                with doc.list:
                    doc.ordered_item(bold("Bold List Item"))
                    doc.paragraph(
                        "Mauris vel magna id ipsum consequat vulputate. Nulla id turpis non eros tincidunt aliquet eleifend id orci. Proin leo odio, finibus nec fermentum vitae, bibendum sed eros. Sed sapien lectus, euismod vitae risus in, lobortis rutrum purus. Proin at velit ut risus euismod aliquam. Donec vitae iaculis mi. Etiam quis aliquet ligula. Ut gravida velit ac porttitor sagittis. Donec pretium lacus in nibh malesuada, at rutrum mi sollicitudin. Sed maximus sodales elit non egestas. Curabitur nec efficitur libero. Nullam mattis euismod ligula nec cursus."
                    )
                    doc.ordered_item(bold("Bold List Item"))
                    doc.ordered_item(bold("Bold List Item"))
    
        assert doc.render() == file.read()
    