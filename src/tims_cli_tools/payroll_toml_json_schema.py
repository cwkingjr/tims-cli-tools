JSON_SCHEMA_STR = """
{
  "$schema": "http://json-schema.org/schema#",
  "additionalProperties": false,
  "type": "object",
  "properties": {
    "processing_info": {
      "type": "object",
      "properties": {
        "create_crew_spreadsheets": {
          "type": "string"
        },
        "process_logging": {
          "type": "string"
        }
      },
      "required": [
        "create_crew_spreadsheets",
        "process_logging"
      ]
    },
    "pay_type": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "pay_type_key": {
            "type": "string"
          },
          "guyed": {
            "type": "number"
          },
          "ss": {
            "type": "number"
          },
          "mp": {
            "type": "number"
          },
          "mp_cans": {
            "type": "number"
          }
        },
        "required": [
          "guyed",
          "mp",
          "mp_cans",
          "name",
          "pay_type_key",
          "ss"
        ]
      }
    },
    "additional_pay": {
      "type": "object",
      "properties": {
        "extra_cans_each": {
          "type": "number"
        },
        "hvf": {
          "type": "number"
        },
        "lighting_inspection": {
          "type": "number"
        },
        "migratory_bird": {
          "type": "number"
        },
        "windsim": {
          "type": "number"
        },
        "ttp_inititial_reading": {
          "type": "number"
        },
        "tension_700": {
          "type": "number"
        },
        "tension_850": {
          "type": "number"
        },
        "tension_1000": {
          "type": "number"
        },
        "hr_pay_per_hour": {
          "type": "number"
        }
      },
      "required": [
        "extra_cans_each",
        "hr_pay_per_hour",
        "hvf",
        "lighting_inspection",
        "migratory_bird",
        "tension_1000",
        "tension_700",
        "tension_850",
        "ttp_inititial_reading",
        "windsim"
      ]
    },
    "crew_lead": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "spreadsheet_name": {
            "type": "string"
          },
          "pay_type_key": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "pay_type_key",
          "spreadsheet_name"
        ]
      }
    },
    "crew_second": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "pay_type_key": {
            "type": "string"
          },
          "crew_lead_name": {
            "type": "string"
          }
        },
        "required": [
          "crew_lead_name",
          "name",
          "pay_type_key"
        ]
      }
    }
  },
  "required": [
    "additional_pay",
    "crew_lead",
    "crew_second",
    "pay_type",
    "processing_info"
  ]
}
"""
