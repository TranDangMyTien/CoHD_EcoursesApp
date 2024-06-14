import axios from "axios";

const BASE_URL = "https://mtie.pythonanywhere.com/";
//https://mtie.pythonanywhere.com/
//http://192.168.1.12:8000/
// const BASE_URL = "http://192.168.1.12:8000/";


export const endpoints = {
  'categories': "/categories/",
  'courses': '/courses/',
  'lessons': (courseId) => `/courses/${courseId}/lessons/` , //Dùng cú pháp literal dấu gần số 1 
  'lesson-details': (lessonId) => `/lessons/${lessonId}`,
  'comments': (lessonId) => `/lessons/${lessonId}/get_comments/`,
  'register': '/users/',
  'login': '/o/token/',
  'current-user': '/users/current-user/'
};

//Xác thực người dùng 
export const authApi = (token) => {
  return axios.create({
      baseURL: BASE_URL,
      headers: {
          Authorization: `Bearer ${token}`
      }
  });
}

export default axios.create({
  baseURL: BASE_URL,
});
