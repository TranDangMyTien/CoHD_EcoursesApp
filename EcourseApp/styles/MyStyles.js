import {StyleSheet} from "react-native"
export default StyleSheet.create(
    {
        container:{
            flex: 1,
            marginTop: 60,
            // justifyContent: "center",
            // alignItems: "center"
        },
        subject:{
            fontSize: 30,
            fontWeight: "bold",
            color:"blue",
            justifyContent: "center",
            alignItems: "center"
        }
        , row:{
            flexDirection: "row",
        }, margin:{
            margin: 8
        }, avatar:{
            width: 80,
            height: 80,
            borderRadius: 20,
        },wrap:{
            flexWrap: "wrap"
        }

    }
);