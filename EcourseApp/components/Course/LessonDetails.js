import {  ActivityIndicator, Text, View, useWindowDimensions, ScrollView , LogBox, Image} from "react-native";
import MyStyles from "../../styles/MyStyles";
import { Card, Chip, List } from "react-native-paper";
import {useState, useEffect  } from "react";
import APIs, { endpoints } from "../../configs/APIs";
// import RenderHTML from "react-native-render-html";
//import RenderHTML from './RenderHTML';
// import RenderHTML, { renderers } from 'react-native-render-html';
//import { ScrollView } from "react-native-gesture-handler";
//import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { isCloseToBottom } from "../Utils/Utils";
import RenderHTML from "react-native-render-html";
import moment from "moment";
import "moment/locale/vi";


//Đóng thông báo warning : Warning từ react-native-render-html
LogBox.ignoreLogs([
    'Warning: TRenderEngineProvider: Support for defaultProps will be removed from function components in a future major release.',
    'Warning: MemoizedTNodeRenderer: Support for defaultProps will be removed from memo components in a future major release.',
    'Warning: TNodeChildrenRenderer: Support for defaultProps will be removed from function components in a future major release.'
  ]);

const LessonDetails = ({route}) => {  //route này nhận giá trị từ lessonId của Lesson 
    const [lesson, setLesson] = useState(null);
    const lessonId = route.params?.lessonId; //params là một object chứa các giá trị truyền vào từ component cha
    const { width } = useWindowDimensions();
    const [comments, setComments] = useState(null); 
    const [loading, setLoading] = useState(false);
    const [page,setPage] = useState(1); //Mặc định là trang số một 

    
    const loadLesson = async () => {
        try {
            let res = await APIs.get(endpoints['lesson-details'](lessonId))
            setLesson(res.data);
        } catch (ex) {
            console.error(ex);
        }
    }

    // //Hàm này không cần nạp cùng lúc với Lesson, chỉ cần nạp khi người ta lướt tới 
    // const loadComments = async () => {
    //     if (page > 0){
    //         let url = `${endpoints['comments'](lessonId)}?page=${page}`
    //         try{
    //             setLoading (true);
    //             let res = await APIs.get(url);
    //             if (page===1)
    //                 setComments(res.data.results);  //Có phân trang 
    //             else if (page > 1)
    //                 setComments(current => {
    //                     return [...current, ...res.data.results]
    //                     });
    //             if(res.data.next === null){
    //                 setPage(0);
    //             }
    //             console.info(res.data.results);

    //         }catch (ex){
    //             console.error(ex)
    //         }finally{
    //             setLoading(false);
    //         }
    //     }
        
    // }

    const loadComments = async () => {
        if (loading || page === 0) return; // Ngăn chặn tải lại nếu đang tải hoặc không còn trang
    
        setLoading(true);
        const url = `${endpoints['comments'](lessonId)}?page=${page}`;
        try {
          let res = await APIs.get(url);
          setComments(current => page === 1 ? res.data.results : [...current, ...res.data.results]);
          setPage(res.data.next === null ? 0 : page + 1);
        } catch (ex) {
          console.error(ex);
        } finally {
          setLoading(false);
        }
    }
    

    useEffect(() => {
        loadLesson();
        setPage(1); // Reset về trang 1 khi lessonId thay đổi
        setComments([]); // Xóa bình luận trước đó
        loadComments(); // Tải bình luận cho bài học mới
    }, [lessonId]);


    const loadMoreInfo = ({nativeEvent}) => {
        if (loading===false && page > 0 && isCloseToBottom(nativeEvent)){
            loadComments();
        }
            
    }


    return(
        
        <View style={[MyStyles.container, MyStyles.margin]}>
            <ScrollView onScroll={loadMoreInfo}>
                {lesson===null?<ActivityIndicator />:<>
                    <Card>
                        <Card.Title title={lesson.subject} titleStyle={[MyStyles.subject, MyStyles.top]}/>
                        <Card.Cover source={{ uri: lesson.image }} />
                        <Card.Content>
                            <View style={MyStyles.row}>
                                {lesson.tags.map(t => <Chip icon='tag' style={MyStyles.margin} key={t.id}>{t.name}</Chip>)}
                            </View>
                            <Text variant="titleLarge">{lesson.subject}</Text>
                            <Text variant="bodyMedium">
                                <RenderHTML contentWidth={width} source={{html: lesson.content}}/>
                            </Text>
                        </Card.Content>
                        
                    
                    </Card>
                </>}
                <View>
                    {comments && <>
                        {comments.map(c => <List.Item key={c.id}
                                title={c.content}
                                description={moment(c.created_date).fromNow()}
                                left={() => <Image source={{uri: c.user.image}} style={MyStyles.avatar} />}
                            />)}
                    </>}
                </View>
            </ScrollView>
            
            
        </View>
        
        
    );
}

export default LessonDetails;

//RenderHTML: dùng để render nội dung HTML trong ứng dụng React Native
//contentWidth: xác định chiều rộng của nội dung HTML được hiển thị, thường được đặt bằng chiều rộng của màn hình hoặc một phần cụ thể của giao diện.
//width là chiều rộng của cửa sổ (screen width), có thể được lấy từ hook useWindowDimensions

//Thuộc tính source chỉ định nguồn HTML cần hiển thị. 
//Nó nhận một đối tượng với thuộc tính html chứa chuỗi HTML cần render.
//lesson.content là chuỗi HTML được hiển thị trong ứng dụng.


//Khi viết map phải có key không sẽ bị lỗi cây DOM 


//                                <RenderHTML contentWidth={width} source={{html: lesson.content}}{...rendererProps}/>
