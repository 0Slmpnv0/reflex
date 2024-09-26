interface Props {
    options: Array<string>,
    dropped: boolean,
}


export default function CustomDropdown({ options, dropped }: Props ) {
    if (!dropped) {
        return
    }

    return (
        <table className="">
            {
                options.map((opt) => (
                    <tr>{opt}</tr>
                ))
            }
        </table>
    )
}