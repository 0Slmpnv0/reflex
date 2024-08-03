import { ReactNode } from "react";


interface Props {
    children: ReactNode;
    onClick: () => void;
    status: 'inactive' | 'active' | 'submitted'
}



export default function Button({ children, onClick, status }: Props) {
    const styles = {
        inactive: 'button-inactive',
        active: 'button-active',
        submitted: 'button-submitted'
    }

    return (
        <button 
        type="submit"
        onClick={status === 'inactive' ? () => {} : onClick}
        className={styles[status]} 
        disabled={status === 'inactive'}
        >{children}</button>
    )
}