import re
from urls import url_patterns

def render_template(template_name, context):
    with open(f'views/{template_name}', 'r') as file:
        template = file.read()
    
    # Handle extends tag
    extends_match = re.search(r'{%\s*extends\s+["\'](.+?)["\']', template)
    if extends_match:
        base_template = extends_match.group(1)
        with open(f'views/{base_template}', 'r') as file:
            base_content = file.read()
        template = re.sub(r'{%\s*block\s+content\s*%}.*?{%\s*endblock\s*%}',
                          lambda m: '{% block content %}' + template + '{% endblock %}',
                          base_content, flags=re.DOTALL)

    # Replace variables
    for key, value in context.items():
        template = template.replace('{{ ' + key + ' }}', str(value))
    
    # Handle for loops
    for loop_match in re.finditer(r'{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%}(.*?){%\s*endfor\s*%}', template, re.DOTALL):
        var_name, iterable_name, loop_content = loop_match.groups()
        if iterable_name in context:
            replacement = ''.join(loop_content.replace('{{ ' + var_name + ' }}', str(item)) for item in context[iterable_name])
            template = template.replace(loop_match.group(), replacement)
    
    # Handle if statements (simple version)
    for if_match in re.finditer(r'{%\s*if\s+(\w+)\s*%}(.*?){%\s*endif\s*%}', template, re.DOTALL):
        condition, content = if_match.groups()
        if condition in context and context[condition]:
            template = template.replace(if_match.group(), content)
        else:
            template = template.replace(if_match.group(), '')

    # Handle links with named URLs
    def url_replacer(match):
        url_name = match.group(1)
        for pattern, _, name in url_patterns:
            if name == url_name:
                return pattern        
        return f"/{url_name}"  # Fallback if no match found

    template = re.sub(r'{%\s*url\s+["\'](\w+)["\']\s*%}', url_replacer, template)



    # Remove any remaining template tags
    template = re.sub(r'{%.*?%}', '', template)
    
    return template
