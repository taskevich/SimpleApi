import React from 'react';
import "./style.scss"
import data from "../../string.json"
import TarifItem from "./TarifItem/TarifItem";
const TarrifsList = () => {
    return(
        <div className="tarifList flex">
            {data.tariffs.map((item) => (
                <TarifItem key={item.title} item={item}/>
            ))}
        </div>
    )
};

export default TarrifsList;