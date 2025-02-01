import './HeadPanel.css'
import './Home.css'
import './bootstrap_5.0.2/css/bootstrap.css';
import logotype from './image/phoneRem.png';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Home() {
    const navigate = useNavigate();

    axios.defaults.headers.post['Content-Type'] ='application/json;charset=utf-8';
    axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
    // console.log(axios.post('http://localhost:5000/check', { "mess": "haushki" }));
    
    // axios.defaults.headers.post['Content-Type'] ='application/json;charset=utf-8';
    // axios.defaults.headers.post['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5000';
    // axios.defaults.headers.post['Access-Control-Allow-Headers'] = 'Content-Type, Authorization';
    axios.post('http://localhost:5000/check', {
        "mess": "haushki"
      })
      .then(response => {
        console.log('Response sent successfully:', response.data);
      })
      .catch(error => {
        console.error('Error sending response:', error);
      });

    const handleGo = () => {
        navigate("/processing");
    };

    return (
        <div class="ho">
            <h1>Home page</h1>
            <h2>h2 tag</h2>
            <div class="row">
                <div class="col-md-6 left">
                    <h1>sf</h1>
                    <p>Вам представлен макета программного средства имитации фотографий с фотоаппаратов известных производителей для анонимизации изображений в сети интернет</p>
                </div>
                <div class="col-md-6">
                    <h1>img will be here</h1>
                    <img src={logotype} class="tel"/>
                </div>
            </div>
            
            <div class="bottom">
                <div class="button" onClick={(e)=> {e.preventDefault(); handleGo();}}>Попробовать</div>
            </div>
        </div>
    );
}   

export default Home;