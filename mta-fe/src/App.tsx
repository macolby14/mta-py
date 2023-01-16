import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";

function fetchNextStopTimes() {
    return [4, 10, 15, 20, 30, 40, 50, 60];
}

type VertifcalFlexContainerProps = {
    children?: React.ReactNode;
};

type FlexItemProps = {
    children?: React.ReactNode;
};

function FlexItem({ children }: FlexItemProps) {
    return <div>{children}</div>;
}

function App() {
    const [nextStops, setNextStops] = useState<number[]>([]);

    useEffect(() => {
        setNextStops(fetchNextStopTimes());
    }, []);

    return (
        <body className="App">
            <div className="NextTimesContainer VerticalFlexContainer">
                {nextStops.map((stopTime) => {
                    return (
                        <div className="NextTimesContainerChild">
                            C {stopTime}
                        </div>
                    );
                })}
            </div>
        </body>
    );
}

export default App;
