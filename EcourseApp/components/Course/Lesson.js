import {View, Text} from "react-native";
import MyStyles from "../../styles/MyStyles";
import { ActivityIndicator} from "react-native-paper";
import APIs, { endpoints } from "../../configs/APIs";
import React, { useState, useEffect } from "react";
import { TouchableOpacity } from "react-native";
import Item from "../Utils/Item";

//Để lấy cái tham số courseId từ bên Course thì có 2 cách 
//1. Dùng tham số route : Người ta tự gõ vào 
//2. Dùng useRoute 
const Lesson = ({route, navigation}) => { //navigation điều hướng qua LessonDetail 
    const [lessons, setLessons] = useState(null); //Không phân trang cho lesson nên làm như này => Nạp một lần 
    //Cái params có thể bị null nên dùng cú pháp để kiểm tra 
    //Null thì kết thúc, không null thì nó lấy 
    const courseId = route.params?.courseId || null; //Dùng cú pháp để kiểm tra null 

    const loadLessons = async () => {
        try{ // Khong phân trang nên làm bình thường 
            let res = await APIs.get(endpoints['lessons'](courseId)); //Phải truyền courseId thì mới ra danh sách bài học 
            setLessons(res.data); //Dùng setLessons để thay đổi state
        }catch (ex){
            console.log(ex);
        }
    }

    useEffect(
        () => {
            loadLessons();
        },[courseId] //Mỗi lần courseId thay đổi thì nó nạp lại 
    );


    return(
        <View style={MyStyles.container}>
            <Text style={MyStyles.subject}>DANH MỤC BÀI HỌC</Text>
            {lessons===null?<ActivityIndicator /> :<>
                {lessons.map(l => <TouchableOpacity key={l.id} onPress={() => navigation.navigate("LessonDetails", {lessonId: l.id})}>
                    <Item instance={l} />
                </TouchableOpacity>)}
            </>}
        </View>
    );
}

export default Lesson; 