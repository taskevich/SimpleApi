import React from 'react';
import "./style.scss"
const TarifItem = ({item}) => {
    return(
        <div className="tarrifItem flex">
            <h3>{item.title}</h3>
            <ul>
                {item.list.map((punkt, index) => (
                    <li key={index}>{punkt}</li>
                ))}
            </ul>
            <p>{item.price}Руб/мес</p>
            <button className="btn">Выбрать</button>
        </div>
    )
};

export default TarifItem;