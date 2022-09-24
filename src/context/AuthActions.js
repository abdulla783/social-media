export const LoginStart = (userCreds) => ({
    type: 'LOGIN_START'
})

export const LoginSuccess = (user) => ({
    type: 'LOGIN_SUCCESS',
    payload: user
})

export const LoginFailure = (error) => ({
    type: 'LOGIN_FAILURE',
    payload: error
})

export const Follow = (user_id) => ({
    type: 'FOLLOW',
    payload: user_id
})

export const UnFollow = (user_id) => ({
    type: 'UNFOLLOW',
    payload: user_id
})