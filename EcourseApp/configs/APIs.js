import axios from "axios";

const BASE_URL = "https://mtie.pythonanywhere.com/";
//https://mtie.pythonanywhere.com/
//http://192.168.1.12:8000/
// const BASE_URL = "http://192.168.1.12:8000/";


export const endpoints = {
  'categories': "/categories/",
  'courses': '/courses/',
};

export default axios.create({
  baseURL: BASE_URL,
});
