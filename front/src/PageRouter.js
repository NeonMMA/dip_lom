import {
    BrowserRouter as Router,
    Route,
    Routes,
    useNavigate,
} from "react-router-dom";
import Home from "./Home";
import Analysis from "./Analysis";
import Processing from "./Processing";


function PageRouter(path="/") {

    return (
        // <Router>
            
            <Routes>
                <Route exact path="/" element={<Home />} />
                <Route exact path="/Home" element={<Home />} />
                <Route exact path="/analysis" element={<Analysis />} />
                <Route exact path="/processing" element={<Processing />}/>
                {/* <Route path="/login" element={<Login />} />
                {(role === "devop" || role === "distributing") && <Route path="/upload" element={<Upload />} />}
                <Route path="/statistic" element={(role === "devop" || role === "distributing")?<Statistics /> : <WorkerStatisticsPage role={role}/>} />
                
                <Route path="/lessons" element={<Lessons />} />
                <Route path="/chat" element={<Notifications />} />
                {(role === "devop" || role === "distributing") && <Route path="/duty" element={<DutyForm />} />}
                <Route path="/rabstat" element={<WorkerStatisticsPage role={role}/>} /> */}
            </Routes>
        // </Router>
    )
}
    export default PageRouter;