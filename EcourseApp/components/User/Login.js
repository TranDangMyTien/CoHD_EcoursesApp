import { View, Text } from "react-native";
import { Button, TextInput } from "react-native-paper";
import MyStyles from "../../styles/MyStyles";
import React, { useContext } from "react";
import APIs, { authApi, endpoints } from "../../configs/APIs";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useNavigation } from "@react-navigation/native";
import { MyDispatchContext } from "../../configs/Contexts";

const Login = () => {
    const [user, setUser] = React.useState({});
    const fields = [{
        "label": "Tên đăng nhập",
        "icon": "account",
        "name": "username"
    }, {
        "label": "Mật khẩu",
        "icon": "eye",
        "name": "password",
        "secureTextEntry": true
    }];
    const [loading, setLoading] = React.useState(false);
    const nav = useNavigation();
    const dispatch = useContext(MyDispatchContext);

    const updateSate = (field, value) => {
        setUser(current => {
            return {...current, [field]: value}
        });
    }

    const login = async () => {
        setLoading(true);
        try {
            let res = await APIs.post(endpoints['login'], {
                ...user,
                'client_id': '5H9NegdD3IUHpYLYtDLB5QFt9x1rV1Q71i8JH2l9',
                'client_secret': 'jCEA9lfZ7v4b7uXrvlZEaaeR3eQGc7dX81h9tkXemWmRGPCoHFzT12S2xnoA24B5vAAx88VbAjkvcTiSipOpGlVxlJNGiRaaFRpheUbDuEAl7bZ5Lb8ZX3Xs1U2p1eGg',
                'grant_type': 'password'
            });
            console.info(res.data);

            await AsyncStorage.setItem("token", res.data.access_token);
            
            setTimeout(async () => {
                let user = await authApi(res.data.access_token).get(endpoints['current-user']);
                console.info(user.data);

                dispatch({
                    'type': "login",
                    'payload': user.data
                })

                nav.navigate('Home');
            }, 100);
        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }   
    }

    return (
        <View style={[MyStyles.container, MyStyles.margin]}>
            <Text style={MyStyles.subject}>ĐĂNG NHẬP NGƯỜI DÙNG</Text>
            {fields.map(c => <TextInput secureTextEntry={c.secureTextEntry} value={user[c.name]} onChangeText={t => updateSate(c.name, t)} style={MyStyles.margin} key={c.name} label={c.label} right={<TextInput.Icon icon={c.icon} />} />)}
            <Button icon="account" loading={loading} mode="contained" onPress={login}>ĐĂNG NHẬP</Button>
        </View>
    );
}

export default Login;