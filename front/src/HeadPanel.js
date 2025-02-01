import { useEffect } from 'react';
import './HeadPanel.css';
import { Link, useLocation } from 'react-router-dom';
import logotype from './image/logo192.png';

function HeadPanel() {
    
    return (
        <header class="header">
        <div class="logo">
            {/* <img src="logo.png" alt="Shadow Logo"> */}
            <img src={logotype}/>
            <span>SHADOWRAZE</span>
        </div>
        <nav class="navigation">
            <Link to="/" class={useLocation().pathname === "/"?"active" : ""}>Главная</Link>
            <Link to="/analysis" class={useLocation().pathname === "/analysis"?"active" : ""}>Анализ</Link>
            <Link to="/processing" class={useLocation().pathname === "/processing"?"active" : ""}>Обработка</Link>
            <Link to="/portfolio" class={useLocation().pathname === "/portfolio"?"active" : ""}>Портфолио</Link>
            <Link to="/contact" class={useLocation().pathname === "/contact"?"active" : ""}>Контакты</Link>
        </nav>
        <div class="header-icons">
        </div>
    </header>
    );
}

export default HeadPanel;