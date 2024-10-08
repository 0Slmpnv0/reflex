import { useState } from "react";

interface Props {
  name: string;
  fieldType: "number" | "tag" | "checkbox" | "percent" | "unselected";
  onDelete: (id: string) => void;
  onChangeType: (newType: "number" | "tag" | "checkbox" | "percent") => void;
  onRename: (newName: string, id: string) => void;
  selectOtions?: Array<string>;
  id: string;
}

export default function FieldSettings({
  name,
  fieldType,
  onDelete,
  onChangeType,
  onRename,
  id,
}: Props) {
  const [currentType, setCurrentType] = useState(fieldType);

  let possible_field_types = ["tag", "checkbox", "percent", "number"];

  let selectorStyles = "type-selector";

  switch (currentType) {
    case "unselected":
      selectorStyles += " bg-gray-500";
      break;
    case "tag":
      selectorStyles += " bg-red-600";
      break;
    case "checkbox":
      selectorStyles += " bg-violet-700";
      break;
    case "percent":
      selectorStyles += " bg-amber-600";
      break;
    case "number":
      selectorStyles += " bg-indigo-600";
      break;
  }

  return (
    <div className="field-setting">
      {/* <textarea
        name={name}
        defaultValue={name}
        id={id}
        rows={1}
        onBlur={(e) => {
          onRename(e.target.value, id);
        }}
      ></textarea> */}

      <input type="text" defaultValue={name} />

      <select
        name="select"
        id={id}
        className={selectorStyles}
        onChange={(e) => {
          setCurrentType(
            e.target.value as "number" | "tag" | "checkbox" | "percent"
          );
          onChangeType(
            e.target.value as "number" | "tag" | "checkbox" | "percent"
          );
        }}
      >
        {currentType === "unselected" ? (
          <option value="unselected" hidden selected>
            unselected
          </option>
        ) : (
          <option value="unselected" hidden>
            unselected
          </option>
        )}
        {possible_field_types.map((fieldType: string) =>
          fieldType === currentType ? (
            <option key={fieldType} value={currentType} selected>
              {currentType}
            </option>
          ) : (
            <option key={fieldType} value={fieldType}>
              {fieldType}
            </option>
          )
        )}
      </select>

      <svg
        fill="#000000"
        viewBox="0 0 32 32"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="none"
        onClick={() => onDelete(id)}
      >
        <path d="M18.8,16l5.5-5.5c0.8-0.8,0.8-2,0-2.8l0,0C24,7.3,23.5,7,23,7c-0.5,0-1,0.2-1.4,0.6L16,13.2l-5.5-5.5  c-0.8-0.8-2.1-0.8-2.8,0C7.3,8,7,8.5,7,9.1s0.2,1,0.6,1.4l5.5,5.5l-5.5,5.5C7.3,21.9,7,22.4,7,23c0,0.5,0.2,1,0.6,1.4  C8,24.8,8.5,25,9,25c0.5,0,1-0.2,1.4-0.6l5.5-5.5l5.5,5.5c0.8,0.8,2.1,0.8,2.8,0c0.8-0.8,0.8-2.1,0-2.8L18.8,16z" />
      </svg>
    </div>
  );
}
