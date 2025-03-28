string = '''[
  {
    "name": "string",
    "type": "tag",
    "options": [
      "string"
    ],
    "is_required": false,
    "display": {
      "is_display_field": true,
      "is_positive": true
    }
  },
  {
    "name": "string2",
    "type": "number",
  },
  {
    "name": "check",
    "type": "checkbox",
    "is_required": false,
    "display": {
      "is_display_field": true,
    }
  },
  {
    "name": "string",
    "type": "tag",
    "options": [
      "string"
    ],
    "is_required": false,
    "display": {
      "is_display_field": true,
      "is_positive": true
    }
  },
]'''

print(string[200:255])
print('\n')
print(string[249])
