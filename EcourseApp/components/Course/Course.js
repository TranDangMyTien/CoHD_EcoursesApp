import {View, Text, Image, ScrollView, RefreshControl, TouchableOpacity} from "react-native"
import MyStyles from "../../styles/MyStyles";
import React, { useState, useEffect } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { ActivityIndicator, Searchbar } from "react-native-paper";
import { Chip, List } from "react-native-paper";
import Item from "../Utils/Item";
import { isCloseToBottom } from "../Utils/Utils";
import "moment/locale/vi";


const Course = ({navigation}) => {
  const [categories, setCategories] = useState(null);
  const [courses,setCourse] = useState([]);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState("");
  const [cateId, setCateId] = useState("");
  const [page,setPage] = useState(1); //Mặc định là trang số một 


  const loadCates = async () => {
    try{
      let res = await APIs.get(endpoints['categories']);
      setCategories(res.data);
    }catch (ex){
      console.error(ex);
    }
  }

  const loadCourses = async () => {
    if (page > 0)
    {

      let url = `${endpoints['courses']}?q=${q}&category_id=${cateId}&page=${page}`;
      // //Trên Server làm rồi nên không cần if else nữa 
      // let url = endpoints["courses"];
      // if (q && cateId) {
      //   url += `?q=${q}&category_id=${cateId}&page=${page}`;
      // } else if (q) {
      //   url += `?q=${q}&page=${page}`;
      // } else if (cateId) {
      //   url += `?category_id=${cateId}&page=${page}`;
      // }

      // if (q && cateId) {
      //   url += `?q=${q}&category_id=${cateId}`;
      // } else if (q) {
      //   url += `?q=${q}&`;
      // } else if (cateId) {
      //   url += `?category_id=${cateId}`;
      // }

      try{
        setLoading (true);
        let res = await APIs.get(url);
        // setCourse(res.data.results); // lấy dữ liệu theo kiểu phân trang (từ phản hồi của người dùng)
        //Nếu là page số 1 thì đè thẳng lên luôn 
        //Nếu là page số 2 thì chỉ nối đuôi hiện thêm chứ không ghi đè 
        if (page===1)
          setCourse(res.data.results);
        else if (page > 1)
        //current số phần tử hiện tại trên màng hình 
          setCourse(current => {
            return [...current, ...res.data.results]
          });

        //Nếu có next thì cho nạp dữ liệu tiếp, không thì thôi 
        if(res.data.next === null) { //Nếu next = null 
          setPage(0); //page bằng không thì ko cho nạp dữ liệu nữa 
        } 
         

      }catch(ex){
        console.error(ex);
      }finally{
        setLoading(false);
      }
    }
  }

  // const search = (id, setCateId) => {
  //   setCateId(id);
  // };

  const search = (value, callback) => {
    setPage(1);
    callback(value)
  }
  useEffect(
    () => {
      loadCates();
    },[]
  );

  useEffect(
    () => {
      loadCourses();
    },[q,cateId,page]
  )

  //Hàm ứng dụng để load course 
  const loadMore = ({nativeEvent}) => {
    // console.info(page)
    // Khi đang loading thì không cho nạp trang => sai số trang 
    if (loading===false && page > 0 && isCloseToBottom(nativeEvent)) { //Khi page > 0 thì mới tiến hành cập nhật dữ liệu 
      setPage(page + 1);
    }
  }

  // //Kiểm tra nó kéo tới phần chân điện thoại chưa 
  // //Hàm đo màn hình => Hỗ trợ phần lazy, trượt tới đâu thấy sản phẩm tới đó 
  // const isCloseToBottom = ({layoutMeasurement, contentOffset, contentSize}) => {
  //   const paddingToBottom = 20;
  //   return layoutMeasurement.height + contentOffset.y >=
  //     contentSize.height - paddingToBottom;
  // };

  

  return(
    <View style={MyStyles.container}>
      <Text style={MyStyles.subject}>DANH MỤC KHÓA HỌC</Text>
      <View style={[MyStyles.row, MyStyles.wrap]}>
      <Chip mode={!cateId ? "outlined" : "flat"} style={MyStyles.margin} icon="tag" onPress={() => search("", setCateId)}>Tất cả</Chip>
       {categories===null?<ActivityIndicator/>:<>
          {categories.map(c => <Chip mode={c.id === cateId ? "outlined" : "flat"} key={c.id} onPress={() => search(c.id, setCateId)} style={MyStyles.margin} icon="shape-outline">{c.name}</Chip>)}
      </>}
      </View>
      
      <View>
        <Searchbar
          placeholder="Tìm kiếm khóa học..."
          value={q}
          onChangeText={(t) => search(t, setQ)}
        />
      </View>

      <ScrollView onScroll={loadMore}>
        <RefreshControl onRefresh={() => loadCourses()} />
        {loading && <ActivityIndicator />}
        {courses.length > 0 && courses.map(c => <TouchableOpacity key={c.id} onPress={() => navigation.navigate("Lesson",{'courseId':c.id})}>
          <Item instance={c} />
        </TouchableOpacity>)}
        {loading && page > 1 && <ActivityIndicator/>}
      </ScrollView>
   
    </View>
  );
}

export default Course;


//Searchbar Đây là component từ thư viện react-native-paper được sử dụng để tạo một thanh tìm kiếm
//Thuộc tính placeholder đặt nội dung mẫu hoặc gợi ý trong thanh tìm kiếm
//Thuộc tính onChangeText hàm xử lý được gọi mỗi khi người dùng thay đổi nội dung của thanh tìm kiếm


//onScroll : bắt đối tương đang trượt 


//onRefresh thì load course mới về 

//key={c.id} phải đưa lên thằng cha TouchableOpacity

//Điều hướng bằng navigation 


// Khi nhấn vào mỗi course thì onPress{() => navigation.navigate("Lesson",{'courseId':c.id})} thì nó sẽ điều hướng đến Lesson (qua bên Stack của App.js trước)

//      <Text style={MyStyles.subject}>DANH MỤC KHÓA HỌC</Text>
