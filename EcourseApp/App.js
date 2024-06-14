import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import Course from "./components/Course/Course";
import LessonDetails from "./components/Course/LessonDetails";
import Register from "./components/User/Register";
import Login from "./components/User/Login";
import { Icon } from "react-native-paper";
import { MyDispatchContext, MyUserContext } from "./configs/Contexts";
import { useContext, useReducer } from "react";
import Profile from "./components/User/Profile";
import MyUserReducer from "./configs/Reducers";
import Lesson from "./components/Course/Lesson";


//Cài đăt stack 
const Stack = createStackNavigator();

//Chia màn hình của Tab Home 
const MyStack = () => {
  return (
    <Stack.Navigator screenOptions={{headerShown: false}}> 
      <Stack.Screen name="Course" component={Course} />
      <Stack.Screen name="Lesson" component={Lesson} />
      <Stack.Screen name="LessonDetails" component={LessonDetails} />

    </Stack.Navigator>
  );
}

const Tab = createBottomTabNavigator();
const MyTab = () => {
  const user = useContext(MyUserContext);
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={MyStack} options={{title: 'Khóa học', tabBarIcon: () => <Icon size={30} color="blue" source="home" />}} />

      {user===null?<>
        <Tab.Screen name="Register" component={Register} options={{title: 'Đăng ký', tabBarIcon: () => <Icon size={30} color="blue" source="account" />}} />
        <Tab.Screen name="Login" component={Login} options={{title: 'Đăng nhập', tabBarIcon: () => <Icon size={30} color="blue" source="login" />}} />
      </>:<>
        <Tab.Screen name="Profile" component={Profile} options={{title: user.username, tabBarIcon: () => <Icon size={30} color="blue" source="account" />}} />
      </>}
      
    </Tab.Navigator>
  );
}



export default function App() {
  const [user, dispatch] = useReducer(MyUserReducer, null);

  return (
    <NavigationContainer>
      <MyUserContext.Provider value={user}>
        <MyDispatchContext.Provider value={dispatch}>
          <MyTab />
        </MyDispatchContext.Provider>
      </MyUserContext.Provider>
    </NavigationContainer>
  );
}

//Tất cả cái gì muốn điều hướng thì dùng NavigationContainer 

//screenOptions={{headerShown: false}} : Ẩn đi cái Stack 