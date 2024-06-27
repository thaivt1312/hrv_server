import {
    BrowserRouter,
    Routes,
    Route,
    Navigate,
} from 'react-router-dom'

import LoginPage from '../pages/Login';
import RegisterPage from '../pages/Register';

import AdminPage from '../pages/admin';
import AccountListPage from '../pages/admin/AccountList';

import UserPage from '../pages/user';
import DeviceListPage from '../pages/DeviceList';
import DetailPage from '../pages/Detail';

const Router = () => {
    let user_token = typeof window !== 'undefined' && (window.localStorage.getItem("data") && window.localStorage.getItem("data") !== 'null') 
        ? JSON.parse(window.localStorage.getItem("data")).user_token
        : "";
    let admin_token = typeof window !== 'undefined' && (window.localStorage.getItem("data") && window.localStorage.getItem("data") !== 'null') 
        ? JSON.parse(window.localStorage.getItem("data")).admin_token
        : "";
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' 
                    element={
                        admin_token ? 
                        <AdminPage />
                        : user_token ? 
                        <UserPage />
                        : <Navigate to={"/login"} />
                    } 
                />
                <Route path="/register" 
                    element={
                        (user_token || admin_token) ?
                        <Navigate to={'/'} />
                        : <RegisterPage/>
                    }
                />

                <Route path='/detail/:id' element={<DetailPage />} />

                <Route path='/account-list'
                    element={
                        admin_token ?
                        <AccountListPage />
                        : <Navigate to={'/'} />
                    }
                />
                
                {
                    (!user_token && !admin_token) ?
                        <Route path="/login" element={<LoginPage />} /> : <></>
                }
                <Route path='/device-list' 
                    element={
                        (!user_token && !admin_token) ?
                        <Navigate to={'/login'} />
                        : <DeviceListPage />
                    }
                />

                <Route path="*" 
                    element={
                        (user_token || admin_token) ?
                        <Navigate to={'/'} />
                        : <Navigate to={'/login'} />
                    }
                />
            </Routes>
        </BrowserRouter>
    )
}

export default Router