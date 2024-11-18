interface Props {
  options: Array<string>;
  // id: string,
  dropped: boolean;
  current_option: string;
  onClick: (value: string) => void;
}

export default function CustomDropdown({
  options,
  dropped,
  current_option,
  onClick,
}: Props) {
  if (!dropped) {
    return;
  }

  return (
    <table className="">
      {options.map((opt) =>
        opt === current_option ? (
          <tr key={opt} className="current" onClick={() => onClick(opt)}>
            {opt}
          </tr>
        ) : (
          <tr key={opt} className="option" onClick={() => onClick(opt)}>
            {opt}
          </tr>
        )
      )}
    </table>
  );
}
