import CustomDropdown from "./CustomDropdown";
import { useEffect, useState } from "react";

interface Props {
  name: string;
  current_option: string;
  options: string[];
  id: string;
}

export default function TagField({ name, current_option, options, id }: Props) {
  const [isSelectorDropped, setIsSelectorDropped] = useState<boolean>(false);
  const [currentOption, setCurrentOption] = useState<string>(current_option);

  useEffect(() => {
    if (document.activeElement !== document.body) {
      setIsSelectorDropped(false);
    }
  }, []);

  return (
    <div
      className="tag-wrapper"
      onBlur={(event: React.FocusEvent<HTMLDivElement>) => {
        console.log(event.relatedTarget)
      }}
    >
      <h1>{name}</h1>
      <div className="tag flex-col">
        <div className="flex">
          <input
            type="text"
            defaultValue={currentOption === "unselected" ? "" : currentOption}
            onClick={() => {
              setIsSelectorDropped(true);
            }}
            className="w-full"
          />
        </div>

        <CustomDropdown
          options={options}
          current_option={currentOption}
          dropped={isSelectorDropped}
          onClick={(value: string) => {
            setIsSelectorDropped(false);
            setCurrentOption(value);
          }}
        />
      </div>
    </div>
  );
}