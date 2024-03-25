import React from 'react';
import "./style.scss"
import data from "../../string.json"
import TarrifItem from "./TarifItem/TarrifItem";
const TarrifsList = () => {
    return(
        <div className="tarifList flex">
            {data.tariffs.map((item) => (
                <TarrifItem key={item.title} item={item}/>
            ))}
        </div>
    )
};

export default TarrifsList;