import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import {StatusBar} from 'expo-status-bar'
import Course from './components/Course/Course';
import Lesson from './components/Course/Lesson';
import 'react-native-gesture-handler';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LessonDetails from './components/Course/LessonDetails';


//Cài đăt stack 
const Stack = createNativeStackNavigator();

//Chia màn hình 
const MyStack = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={Course} />
      <Stack.Screen name="Lesson" component={Lesson} />
      <Stack.Screen name="LessonDetails" component={LessonDetails} />

    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <NavigationContainer>
      <MyStack/> 
    </NavigationContainer>
  );
}

//Tất cả cái gì muốn điều hướng thì dùng NavigationContainer 

