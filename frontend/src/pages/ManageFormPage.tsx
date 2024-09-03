import FieldSettings from "../components/FieldSettings";

type Field = {
  type: "tag" | "num" | "checkbox" | "percent";
  is_required?: boolean; // experimental. In future Ill support unrequired fields, but now idk how to make it not affect the Insights
  display: {
    is_display_field: boolean;
    is_positive?: boolean; // another experimental thing. In calendar I am going to display some fancy styled days/months items green if the value positive and red if negative
  };
};

let example_form_data: { [key: string]: Field } = {
  "How do I feel today?": {
    type: "num",
    display: {
      is_display_field: false,
    },
  },
  "How many minutes did I exercise?": {
    type: "num",
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
  // field_ data = fetch('backend/form_structure') - coming soon... (not soon at all.)

  const field_data = example_form_data;

  return (
    <div className="wrapper gap-7">
      <h1 className="text-6xl mt-4 mb-20">Manage form </h1>
      <FieldSettings
        name="How do I feel today?"
        type="tag"
        onChangeType={() => alert("hui")}
        onDelete={() => alert("pidor")}
        selectOtions={["asdf", "asdfasdf"]}
        selectorId="1"
      />
    </div>
  );
}
