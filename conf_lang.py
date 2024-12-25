import re
from xml.etree import ElementTree

def parse_config_string(xml_string):
    """Parses the XML string, handling comments and constants."""
    
    def remove_comments(text):
        # Remove multiline comments
        text = re.sub(r'\{\{!--.*?--\}\}', '', text, flags=re.DOTALL)
        # Remove single line comments
        text = re.sub(r'NB\..*?\n', '\n', text)
        return text
    
    xml_string = remove_comments(xml_string)

    class ConfigLanguage:

        def __init__(self):
            self.constants = {}
        
        def parse_xml(self, xml_string):
            try:
              root = ElementTree.fromstring(xml_string)
              output = self.process_element(root)
              return output
            except ElementTree.ParseError as e:
              print(f"Error parsing XML: {e}")
              return None
            
        def process_element(self, element):
            output = ""
            for child in element:
                if child.tag == 'constant':
                    name = child.attrib.get('name')
                    value = child.attrib.get('value')
                    if name and value:
                        try:
                            self.process_constant(name, value)
                        except Exception as e:
                            print(f"Error process constant: {e}")
                    else:
                        print("Invalid constant definition: constant should have 'name' and 'value' attributes.")

                elif child.tag == 'expression':
                    text = child.text.strip() if child.text else ''
                    try:
                        output += self.process_expression(text)
                    except Exception as e:
                        print(f"Error process expression: {e}")
                    output += "\n"

                elif child.tag == 'text':
                  text = child.text.strip() if child.text else ''
                  output += self.process_text(text) + "\n"

                output += self.process_element(child)
                if child != element[-1]:
                    output += "\n"
            return output

        def process_text(self, text):
           output = ""
           tokens = re.findall(r"(@\{[_a-zA-Z][_a-zA-Z0-9]*\}|[^@{}]+)", text)
           for token in tokens:
               if token.startswith("@{") and token.endswith("}"):
                   const_name = token[2:-1]
                   if const_name in self.constants:
                      output += str(self.constants[const_name])
                   else:
                       raise ValueError(f"Undefined constant '{const_name}'")
               else:
                  output += self.escape_special_chars(token)
           return output



        def process_constant(self, name, value):
          if not re.match(r"^[_a-zA-Z][_a-zA-Z0-9]*$", name):
            raise ValueError(f"Invalid constant name: '{name}'. Must start with letter or underscore and contain only letters, numbers, or underscores.")

          try:
            parsed_value = self.parse_value(value)
            self.constants[name] = parsed_value
          except Exception as e:
             raise Exception(f"Error parsing constant value '{value}': {e}")

        def process_expression(self, text):
            output = ""
            tokens = re.findall(r"(@\{[_a-zA-Z][_a-zA-Z0-9]*\}|[^@{}]+)", text)
            for token in tokens:
                if token.startswith("@{") and token.endswith("}"):
                    const_name = token[2:-1]
                    if const_name in self.constants:
                        output += str(self.constants[const_name])
                    else:
                        raise ValueError(f"Undefined constant '{const_name}'")
                else:
                    output += self.escape_special_chars(token)

            return output

        def parse_value(self, value):
          value = value.strip()
          if value.startswith('(') and value.endswith(')'):
                return self.parse_list(value[1:-1])
          elif value.replace('.', '', 1).isdigit():
            try:
                return int(value)
            except ValueError:
                return float(value)
          else:
              return value # Return value if it's not a list, number

        def parse_list(self, list_str):
            items = []
            current_item = ""
            level = 0
            for char in list_str:
                if char == '(':
                    level += 1
                    current_item += char
                elif char == ')':
                    level -= 1
                    current_item += char
                elif char == ' ' and level == 0:
                    if current_item:
                        items.append(self.parse_value(current_item))
                        current_item = ""
                else:
                    current_item += char

            if current_item:
                items.append(self.parse_value(current_item))
            return items

        def escape_special_chars(self, text):
            text = text.replace('\\n', '\n')
            return text

    config_parser = ConfigLanguage()
    return config_parser.parse_xml(xml_string)