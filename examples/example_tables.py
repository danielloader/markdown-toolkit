from markdown_toolkit import MarkdownDocument

doc = MarkdownDocument()
# You can use a table as a context manager and lazily add rows
with doc.table(titles=["Apple Type", "Grown Count"], sort_by="Grown Count") as table:
    table.add_row(apple_type="Granny Smith", grown_count=3)
    table.add_row(apple_type="Golden Delicious", grown_count=1)

with doc.table(titles=["Ticker", "Stock Percentage"]) as table:
    table.add_row(ticker="AAPL", stock_percentage="7.14%")
    table.add_row(ticker="MSFT", stock_percentage="6.1%")
    table.add_row(ticker="AMZN", stock_percentage="3.8%")
    table.add_row(ticker="TSLA", stock_percentage="2.5%")
    table.add_row(ticker="GOOGL", stock_percentage="2.2%")

# Or render a list of dictionaries in a table in one go
raw_table_data = [
    {"Major": "Biology", "GPA": "2.4", "Name": "Edward"},
    {"Major": "Physics", "GPA": "2.9", "Name": "Emily"},
    {"Major": "Mathematics", "GPA": "3.5", "Name": "Sarah"},
]
doc.table(raw_table_data)

with open("examples/example_tables.md", "w", encoding="UTF-8") as file:
    file.write(doc.render())
