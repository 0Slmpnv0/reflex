// TODO: Refactor my shit code, make google auth work


import { useState } from 'react'
import Button from './Button'


interface fieldProps {
    value: string,
    error: {
        status: boolean,
        message: string
    }
}


function validateField(field: string, fieldType: 'login' | 'password'): fieldProps {
    const forbidden_login_symbols: Array<string> = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '[', ']', '{', '}', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/']
    let value = false
    let message = ''

    if (field.length === 0) {
        value = true
        message = 'Field is required'
    }

    else if (fieldType === 'login') {

        if (field.length <= 15 && field.length >= 5) {
            forbidden_login_symbols.forEach((symbol) => {
                if (field.includes(symbol)) {
                    value = true
                    message = 'Login must not include special symbols'
                }
            })
        } 
        else {
            value = true
            message = 'Login length must be between 5 and 15 symbols'
        }
    }

    else {
        if (field.length > 30) {
            value = true
            message = 'Password is too long'
        }
        else if (field.length < 6) {
            value = true
            message = 'Password is too short'
        }
    }


    return {
        value: field,
        error: {
            status: value,
            message: message
        }
    }
}


export default function Login() {
    const [login, setLogin]= useState<fieldProps>({  
        value: '',
        error: {
            status: false,
            message: ''
        }
    })
    const [password, setPassword]= useState<fieldProps>({
        value: '',
        error: {
            status: false,
            message: ''
        }
    })

    const handleClick = () => {
        alert('Pretending to send the data to backend')
    }

    return (
            <form className='reg'>
                <div className='field'>
                    <h3 className='text-left'>Login</h3>
                    <input  
                    className='input mt-1' 
                    type="text" 
                    id='login' 
                    onChange={
                        e => {
                            setLogin(validateField(e.target.value, 'login'))
                        }
                    }
                    required />           { /*Without mt-1 "g" almost touches the input*/}
                    <div className='h-6'>
                        <p className={login.error.status ? 'error visible' : 'invisible'}>
                            {login.error.message}
                        </p>
                    </div>  
                </div>

                <div className='field'>
                    <h3 className='text-left'>Password</h3>
                    <input 
                    className='input' 
                    type="password" 
                    id='password'
                    onChange={
                        e => {
                            setPassword(validateField(e.target.value, 'password'))
                        }
                    }
                    required/> 
                    <div className='h-6'>
                        <p className={password.error.status ? 'error visible' : 'invisible'}>
                            {password.error.message}
                        </p>
                    </div>    
                       
                </div>

                <div className='field'>
                    <h3 className='text-left'>Confirm password</h3>
                    <input 
                    className='input mt-1' 
                    type="password" 
                    id='password'
                    onChange={
                        e => {
                            setPassword(validateField(e.target.value, 'password'))
                        }
                    }
                    required/> 
                    <div className='h-6'>
                        <p className={password.error.status ? 'error visible' : 'invisible'}>
                            {password.error.message}
                        </p>
                    </div>    
                       
                </div>


                <Button 
                status={((login.error.status || password.error.status) || (!login.value || !password.value)) ? 'inactive' : 'active'}
                onClick={handleClick}
                >Submit</Button>

                <p className='text-white text-xl'>Or log in with:</p>

                <img src='https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg' alt="Google" className="google-icon"/>
                
                <p className='text-sm m-0'>Other options <br /> coming soon...</p>
       </form>
    )        
}
