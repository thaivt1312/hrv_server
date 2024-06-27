import { Button, Stack, TextField, Typography } from '@mui/material'

import { useFormik } from 'formik'
import * as Yup from 'yup';
import axios from 'axios';
import { adminUrl, config } from "../remotes/Base";

import { toast } from 'react-toastify';

export default function LoginPage({

}) {
    const formik = useFormik({
        initialValues: {
            username: '',
            password: ''
        },
        validationSchema: Yup.object({
            username: Yup
                .string()
                .max(45)
                .required(),
            password: Yup
                .string()
                .max(45)
                .required()
        }),
        onSubmit: (values) => {
            axios.post(`${adminUrl}/login/`,
                {
                    ...values,
                    firebaseToken: localStorage.getItem('firebaseToken'),
                },
                config
            )
                .then((r) => {
                    let data = r?.data;
                    if (data?.success) {
                        toast.success(data?.msg)
                        localStorage.setItem('data', JSON.stringify(data?.data))
                        // window.location.reload()
                    } else {
                        toast.error(data?.msg)
                    }
                    console.log(r)
                })
        }
    })
    return (
        <form
            noValidate
            onSubmit={formik.handleSubmit}>
            <div style={{
                width: '100%',
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                gap: '20px',
            }}>
                <Stack>
                    <Typography variant='h4' textAlign={"center"}>
                        Smartwatch sound prediction system
                    </Typography>
                </Stack>
                <Stack spacing={2}
                    justifyContent={"center"}
                    alignItems={"center"}
                    flex={1}
                    sx={{
                        border: 'solid 1px',
                        borderRadius: '8px',
                        margin: '15% 25%',
                        padding: '20px',
                    }}
                >
                    <TextField
                        size='small'
                        fullWidth
                        name="username"
                        label="Username"
                        type="text"
                        onChange={formik.handleChange}
                        error={!!(formik.touched.username && formik.errors.username)}
                        helperText={formik.touched.username && formik.errors.username}
                    />

                    <TextField
                        size='small'
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        onChange={formik.handleChange}
                        error={!!(formik.touched.password && formik.errors.password)}
                        helperText={formik.touched.password && formik.errors.password}
                    />

                    <Button type='submit'
                        fullWidth 
                        sx={{
                            border: 'solid 1px'
                        }}
                    >
                        Log in
                    </Button>

                </Stack>
            </div>
        </form>
    )
}