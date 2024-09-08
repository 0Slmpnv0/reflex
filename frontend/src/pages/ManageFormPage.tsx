import FieldSettings from "../components/FieldSettings";
import { useState } from "react";

type Field = {
  type: "tag" | "number" | "checkbox" | "percent";
  is_required?: boolean; // experimental. In future Ill support unrequired fields, but now idk how to make it not affect the Insights
  display: {
    is_display_field: boolean;
    is_positive?: boolean; // another experimental thing. In calendar I am going to display some fancy styled days/months items green if the value positive and red if negative
  };
};

let example_form_data: { [key: string]: Field } = {
  "How do I feel today?": {
    type: "number",
    display: {
      is_display_field: false,
    },
  },
  "How many minutes did I exercise?": {
    type: "number",
    display: {
      is_display_field: false,
    },
  },
  "Did I drink enough water?": {
    type: "checkbox",
    display: {
      is_display_field: false,
    },
  },
  "What percentage of time was I productive?": {
    type: "percent",
    display: {
      is_display_field: true,
    },
  },
  "Todays breakfast?": {
    type: "tag",
    display: {
      is_display_field: false,
    },
  },
};

export default function ManageFormPage() {
  // field_data = fetch('backend/form_structure') - coming soon... (not soon at all.)

  let fieldData = example_form_data

  return (
    <div className="wrapper gap-7">
      <h1 className="text-6xl mt-4 mb-20">Manage form </h1>
      {
        Object.entries(fieldData).map(([name, daily_data]) => (
          <FieldSettings 
            key={name}
            name={name}
            fieldType={daily_data.type}
            onChangeType={() => {
              alert('hui')
            }}
            onDelete={() => alert('hui')}
            id=""
          />
        ))
      }
    </div>
  );
}