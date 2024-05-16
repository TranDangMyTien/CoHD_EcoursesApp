import { View, Text, Image, ScrollView, RefreshControl } from "react-native";
import React, { useState, useEffect } from "react";
import { Chip, List } from "react-native-paper";
import APIs, { endpoints } from "../../configs/APIs";
import MyStyles from "../../styles/MyStyles";
import { ActivityIndicator, Searchbar } from "react-native-paper";
import moment from "moment";
import { TouchableOpacity } from "react-native-gesture-handler";
// import Item from "./Item";
import "moment/locale/vi"; //Hỗ trợ tiếng VIỆT
//import là một từ khoá trong JavaScript được sử dụng để nhập các module
//hoặc tệp từ các nguồn khác nhau vào một module hiện tại
//form : là một từ khoá trong import để chỉ ra nguồn mà chúng ta đang import
//../../styles/MyStyles": Đây là đường dẫn tương đối đến tệp hoặc module mà chúng ta muốn import

//Chuẩn code của JS là biến đặt tên theo lạc đà
const Course = () => {
  // Functional components
  const [categories, setCategories] = useState(null);
  // React Hooks => sử dụng trong functional components của React để quản lý trạng thái (state) của component
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [q, setQ] = useState(""); //"" khi tìm kiếm là lấy hết
  const [cateId, setCateId] = useState("");
  const [page, setPage] = useState(1);

  
  const loadCates = async () => {  // Dùng async : Hàm bất đồng bộ
    //Dùng arrow function
    try {
      let res = await APIs.get(endpoints["categories"]); //Gán biến res = /categories
      setCategories(res.data);  //Cập nhật data
    } catch (ex) {
      // Bắt lỗi
      console.error(ex); //Xuất lỗi
    }
  };

  const loadCourses = async () => {
    if (page > 0) {
      setLoading(true); // Trước khi nạp cho loading = true
      let url = `${endpoints["courses"]}?q=${q}&category_id=${cateId}&page=${page}`; //q là biến tìm kiếm, tìm kiếm về subject của course
      try {
        let res = await APIs.get(url);

        if (res.data.next === null) setPage(0);

        if (page === 1) setCourses(res.data.results);
        else
          setCourses((current) => {
            return [...current, ...res.data.results];
          });
      } catch (ex) {
        console.error(ex);
      } finally {
        //Trường hợp kết thúc hoặc bị lỗi
        setLoading(false);
      }
    }
  };
  const search = (id, setCateId) => {
    setCateId(id);
  };

  useEffect(() => {
    loadCates();
  }, []);

  useEffect(() => {
    loadCourses();
  }, [q, cateId, page]); //q thay đổi thì nó gọi lại


  //Trượt đến cuối thì sản phẩm sẽ được đẩy mới lên => Kiểm tra tới phần chân cuối chưa
  const isCloseToBottom = ({
    layoutMeasurement,
    contentOffset,
    contentSize,
  }) => {
    const paddingToBottom = 20;
    return (
      layoutMeasurement.height + contentOffset.y >=
      contentSize.height - paddingToBottom
    );
  };

  const loadMore = ({ nativeEvent }) => {
    if (isCloseToBottom(nativeEvent)) {
      console.info(Math.random());
    }
  };

  return (
    <View style={MyStyles.container}>
      <View style={MyStyles.row}>
        <Text style={MyStyles.subject}>DANH MỤC KHÓA HỌC</Text>
        <Chip
          mode={!cateId ? "outlined" : "flat"}
          style={MyStyles.margin}
          icon="tag"
          onPress={() => search("", setCateId)}
        >
          Tất cả
        </Chip>
        {categories === null ? (
          <ActivityIndicator />
        ) : (
          <>
            {categories.map((c) => (
              <Chip
                mode={c.id === cateId ? "outlined" : "flat"}
                style={MyStyles.margin}
                key={c.id}
                icon="shape-outline"
                onPress={() => search(c.id, setCateId)}
              >
                {c.name}
              </Chip>
            ))}
          </>
        )}
      </View>

      <View>
        <Searchbar
          placeholder="Tìm kiếm khóa học..."
          value={q}
          onChangeText={setQ}
        />
      </View>
      <ScrollView onScroll={loadMore}>  
        <RefreshControl onRefresh={() => loadCourses()} />
        {loading && <ActivityIndicator />}
        {courses.map(c => <List.Item key={c.id} title={c.subject} description={moment(c.created_date).fromNow()}
        left={() => <Image style={MyStyles.avatar} source={{uri: c.image}} />} />)}
        
      </ScrollView>
    </View>
  );
};

export default Course;

//onScroll={loadMore} : Sự kiện đang trượt 