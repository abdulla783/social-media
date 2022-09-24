import './edit.css'
import { TextField, Box } from '@material-ui/core';

export default function EditProfileForm() {
  return (
    <div className='profileForm'>
      <div className='formWrapper'>
        <Box
          component="form"
          sx={{
            '& .MuiTextField-root': { m: 1, width: '25ch' },
          }}
          noValidate
          autoComplete="off"
        >
          <div>
          <TextField
            required
            id="outlined-required"
            label="Email"
            defaultValue=""
            type='email'
            placeholder='Email'
          />
          <TextField
            required
            id="outlined-required"
            label="First Name"
            defaultValue=""
            placeholder='First Name'
          />
          <TextField
            required
            id="outlined-required"
            label="Last Name"
            defaultValue=""
            placeholder='Last Name'
          />
          </div>
          <br />
          <div>
          <TextField
            required
            id="outlined-required"
            label="Username"
            defaultValue="abd"
            placeholder='Username'
            InputProps={{
              readOnly: true,
            }}
          />
          <TextField
            id="outlined-number"
            label="Phone Number"
            type="number"
            placeholder='Phone'
            InputLabelProps={{
              shrink: true,
            }}
          />  
          </div>
        </Box>
      </div>
    </div>
  )
}
