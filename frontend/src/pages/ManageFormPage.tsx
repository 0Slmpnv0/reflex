import FieldSettings from "../components/FieldSettings";
import { useState } from "react";

type Field = {
  name: string;
  type: "tag" | "number" | "checkbox" | "percent" | "unselected";
  is_required?: boolean; // experimental. In future Ill support unrequired fields, but now idk how to make it not affect the Insights
  display: {
    is_display_field: boolean;
    is_positive?: boolean; // another experimental thing. In calendar I am going to display some fancy styled days/months items green if the value positive and red if negative
  };
};

let example_form_data: { [key: string]: Field } = {
  1: {
    name: "How do I feel today?",
    type: "tag",
    display: {
      is_display_field: false,
    },
  },
  2: {
    name: "How many minutes did I exercise?",
    type: "number",
    display: {
      is_display_field: false,
    },
  },
  3: {
    name: "Did I drink enough water?",
    type: "checkbox",
    display: {
      is_display_field: false,
    },
  },
  4: {
    name: "What percentage of time was I productive?",
    type: "percent",
    display: {
      is_display_field: true,
    },
  },
  5: {
    name: "Todays breakfast?",
    type: "tag",
    display: {
      is_display_field: false,
    },
  },
};

export default function ManageFormPage() {
  // fieldData = fetch('backend/form_structure') - coming soon... (not soon at all.)

  const [fieldData, setFieldData] = useState(example_form_data);

  const onRename = (newName: string, id: string) => {
    setFieldData({
      ...fieldData,
      [id]: {
        ...fieldData[id],
        name: newName,
      },
    });
  };

  const onNewField = () => {
    let id = Object.keys(fieldData).length + 1;
    setFieldData({
      ...fieldData,
      [id]: {
        name: "New field",
        type: "unselected",
        display: {
          is_display_field: false,
        },
      },
    });
  };

  const onDelete = (idToDelete: string) => {
    delete fieldData[idToDelete];
    let newData: { [key: string]: Field } = {};

    let i = 1;

    Object.values(fieldData).forEach((currentField) => {
      newData = {
        ...newData,
        [i]: {
          ...currentField,
        },
      };
      i++;
    });
    console.log(newData);
    setFieldData(newData);
  };

  return (
    <div className="wrapper gap-7">
      <h1 className="text-6xl mt-4 mb-20">Manage form </h1>
      {Object.entries(fieldData).map(([id, dailyData]) => (
        <FieldSettings
          key={id.concat(dailyData.name)}
          name={dailyData.name}
          fieldType={dailyData.type}
          onChangeType={(newType) => {
            setFieldData({
              ...fieldData,
              [id]: {
                ...fieldData[id],
                type: newType,
              },
            });
          }}
          onRename={onRename}
          onDelete={onDelete}
          id={id}
        />
      ))}

      {Object.keys(fieldData).length < 5 ? (
        <button className="new-field-button" onClick={onNewField}>
          New field
        </button>
      ) : (
        <p>No more fields available</p>
      )}

      {Object.keys(fieldData).length > 0 ? (
        <button
          className="new-field-button bg-indigo-500 mt-10 text-white hover:bg-indigo-600"
          onClick={() => {
            alert("pretend to send some data to the backend");
          }}
        >
          Sumbit
        </button>
      ) : (
        <></>
      )}
    </div>
  );
}
