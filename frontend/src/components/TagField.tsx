import CustomDropdown from "./CustomDropdown";
import { useState } from "react";

interface Props {
  name: string;
  current_option: string;
  options: string[];
  id: string;
}

export default function TagField({ name, current_option, options, id }: Props) {
  const [isRotated, setIsRotated] = useState<boolean>(false);
  const [isSelectorDropped, setIsSelectorDropped] = useState<boolean>();

  return (
    <div className="tag-wrapper">
      <h1>{name}</h1>
      <div className="tag flex-col">
        <div className="flex">
          <input
            type="text"
            onClick={() => {
            }}
            className="w-full"
          />
          <svg
            className={isRotated ? "w-15 h-10 ml-auto mr-1 rounded-lg hover:bg-slate-300 rotate-180" : "w-15 h-10 ml-auto mr-1 rounded-lg hover:bg-slate-300"}
            onClick={() => {
              setIsSelectorDropped(!isSelectorDropped);
              setIsRotated(!isRotated);
            }}
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 21 21"
          >
            <path
              d="m8.5.5-4 4-4-4"
              fill="none"
              stroke="#000000"
              stroke-linecap="round"
              stroke-linejoin="round"
              transform="translate(6 8)"
            />
            <path
              xmlns="http://www.w3.org/2000/svg"
              d="m8.5.5-4 4-4-4"
              fill="none"
              stroke="#000000"
              stroke-linecap="round"
              stroke-linejoin="round"
              transform="translate(6 8)"
            />
          </svg>
        </div>

        <CustomDropdown options={options} dropped={isSelectorDropped} />
      </div>
    </div>
  );
}
