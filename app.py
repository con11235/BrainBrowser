import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,title = 'Brain Browser',suppress_callback_exceptions=True)

app.head = [
    html.Meta(charSet="utf-8"),
    html.Meta(content="width=device-width, initial-scale=1.0", name="viewport"),
        
    # Custom fonts for this template
    html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,700,700i|Raleway:300,400,500,700,800", rel="stylesheet"),

]


server = app.server