import { useState } from 'react'
import Button from './Button'
import google from '../assets/google.svg'
import { z } from 'zod'


export default function Login() {
    const [status, setStatus] = useState<'inactive' | 'active' | 'submitted'>('active')

    const User = z.object({
        login: z.coerce.string(),
        password: z.coerce.string()
    })

    if (status !== 'submitted') {
        return (
            <form className='login'>
                <div className='field'>
                    <h3 className='text-left'>Login</h3>
                    <input  className='input mt-1' type="text" id='login' required/>           { /*Without mt-1 "g" almost touches the input*/}
                </div>

                <div className='field'>
                    <h3 className='text-left'>Password</h3>
                    <input className='input' type="password" id='password' required/> 
                </div>

                <Button 
                status={status}
                onClick={() => {
                    setStatus('submitted')
                    const login = (document.getElementById('login') as HTMLInputElement).value
                    const password = (document.getElementById('password') as HTMLInputElement).value
                    const user = User.safeParse({login, password})
                    if (user.success) {
                        console.log(user.data)
                    } else {
                        console.log(user.error)
                    }
                }}
                >Submit</Button>

                <p className='text-white text-lg'>Or log in with:</p>

                <a className="login p-0 items-center max-w-fit hover:bg-gray-700" href='hui'>
                    <img src={google} alt="Google" className="google-icon w-24" />
                </a>
                
                <p className='text-sm m-0'>Other options <br /> coming soon...</p>
                
                <a className='text-blue-700 self-end' href=''>Register</a>

       </form>
    )        
    }

    return (
        <h1 className='text-9xl my-auto text-green-800'>Successful!</h1>
    )

}
