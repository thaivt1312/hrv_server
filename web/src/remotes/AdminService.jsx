// import { adminAxios } from './Base';
import axios from "axios";
import { adminUrl, headers } from "./Base";

let config = {
    headers,
    params: null
}
const AdminService = {

    login(body) {
        return axios.post(
            `${adminUrl}/login/`, 
            {... body}, 
            config
        );
    },
    getAccountList() {
        return adminAxios.get(`${adminUrl}/account/`, config);
    },
    addNewAccount(body) {
        return adminAxios.post(`${adminUrl}/account/`, {... body}, config);
    },
    deleteAccount(id) {
        return adminAxios.delete(`${adminUrl}/account/${id}`, config);
    },
};

export default AdminService;
