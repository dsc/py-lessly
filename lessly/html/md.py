from markdown import Markdown

DEFAULT_TEMPLATE = '''\
{doctype}
<html>
<head>
<title>{title}</title>
<meta http-equiv="content-type" content="text/html; charset=utf8"/>
{headers}
<body class="md markdown">
<div class="content">
{body}
<br style="clear:both;">
</div>
<div class="mdpreview log"><!-- ${TM_MARKDOWN:-$MARKDOWN} $* --></div>
</body>
</html>
'''

DEFAULT_DATA = {
    'doctype' : '<!DOCTYPE html>',
    'title'   : '',
}

def render(text, template=DEFAULT_TEMPLATE, template_data={}, options={}):
    opts = dict(extensions=['extra', 'toc', 'headerid', 'meta', 'codehilite(css_class=highlight)'], output_format='html5',)
    opts.update(options)
    
    renderer = Markdown(**opts)
    body = renderer.convert(text)
    
    data = DEFAULT_DATA.copy()
    data.update(template_data)
    data.update(body=body, text=text)
    
    return template.format(data)

