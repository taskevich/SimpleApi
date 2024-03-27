import React from 'react';
import TarrifsList from "../../components/TariffsList/TarrifsList";
import "./style.scss"

const TariffsPage = () => {
    return(
        <section className="tarifs flex">
            <h2>Тарифные планы</h2>
            <TarrifsList/>
        </section>
    )
};

export default TariffsPage;