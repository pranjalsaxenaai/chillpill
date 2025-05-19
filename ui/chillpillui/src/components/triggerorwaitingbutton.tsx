"use client"
import React, { useState } from "react";

type TriggerOrWaitingButtonProps = {
    text: string;
    onClick: (setIconState: React.Dispatch<React.SetStateAction<TriggerOrWaitingButtonState>>) => void;
};

export enum TriggerOrWaitingButtonState{
    Trigger = "trigger",
    Waiting = "waiting",
}

// Icon of a play button
const triggerIcon = (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-5 w-5"
        viewBox="0 0 20 20"
        fill="currentColor"
        aria-hidden="true"
    >
        <path d="M10 2a8 8 0 100 16 8 8 0 000-16zm1.5 11.5V6.5l4.5 3.5-4.5 3.5z" />
    </svg>
);

// Icon of a waiting spinner
const waitingSpinner = (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        className="h-5 w-5 animate-spin"
        viewBox="0 0 24 24"
        fill="currentColor"
        aria-hidden="true"
    >
        <path d="M12 2a10 10 0 100 20 10 10 0 000-20zm1.5 11.5V6.5l4.5 3.5-4.5 3.5z" />
    </svg>
);

const TriggerOrWaitingButton: React.FC<TriggerOrWaitingButtonProps> = ({ text, onClick }) => {
    const [triggerOrWaitingIcon, setTriggerOrWaitingIcon] = useState(TriggerOrWaitingButtonState.Trigger);

    return (
        <button
            type="button"
            onClick={() => onClick(setTriggerOrWaitingIcon)}
            style={{ display: "flex", alignItems: "center", gap: 8 }}
            disabled={triggerOrWaitingIcon === TriggerOrWaitingButtonState.Waiting}
        >
            <span>
                {triggerOrWaitingIcon === TriggerOrWaitingButtonState.Trigger ? triggerIcon : waitingSpinner}
            </span>
            <span>{text}</span>
        </button>
    );
};

export default TriggerOrWaitingButton;

