import TagField from "../components/TagField";


type Field = {
  name: string;
  type: "tag" | "number" | "checkbox" | "percent" | "unselected";
  options?: string[];
  answer: string;
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
    options: ['nice', 'cool', 'horrible', 'exiting'],
    answer: '',
    display: {
      is_display_field: false,
    },
  },
  2: {
    name: "How many minutes did I exercise?",
    type: "number",
    answer: '',
    display: {
      is_display_field: false,
    },
  },
  3: {
    name: "Did I drink enough water?",
    type: "checkbox",
    answer: '',
    display: {
      is_display_field: false,
    },
  },
  4: {
    name: "What percentage of time was I productive?",
    type: "percent",
    answer: '',
    display: {
      is_display_field: true,
    },
  },
  5: {
    name: "Todays breakfast?",
    type: "tag",
    answer: '',
    display: {
      is_display_field: false,
    },
  },
};


export default function DailyReportPage() {
        return (
        <div className="wrapper">
            <h1 className="text-6xl mt-5">How was your day?</h1>
            {
                Object.entries(example_form_data).map(( [id, fieldData] ) => {
                    if (fieldData.type === 'tag') {
                        return (<TagField
                        name={fieldData.name}
                        current_option="unselected"
                        options={fieldData.options? fieldData.options : []}
                        id={id}
                        />)
                    }
                })
            }
       </ div>
       )
}
