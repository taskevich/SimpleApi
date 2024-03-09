import React from 'react';
import "./style.scss"
const TarifItem = ({item}) => {
    return(
        <div className="tarrifItem flex">
            <h3>{item.title}</h3>
            <p>{item.price}Руб/мес</p>
            <button className="btn">Выбрать</button>
        </div>
    )
};

export default TarifItem;