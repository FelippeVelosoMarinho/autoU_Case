import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "../pages/Home";

function AppRoutes() {
    return (
        <Router>
            <Routes>

                <Route index element={<Home />} />

                <Route
                    path="*"
                    element={
                        <div
                            style={{
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "center",
                                alignItems: "center",
                                textAlign: "center",
                            }}
                        >
                            <h1>
                                Not Found
                                <br />
                                --- 404 ---
                            </h1>
                        </div>
                    }
                />
            </Routes>
        </Router>
    );
}

export default AppRoutes;