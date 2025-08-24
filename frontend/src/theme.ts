import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  shape: { borderRadius: 12 },
  palette: {
    background: { default: '#fafafa', paper: '#ffffff' },
  },
  components: {
    MuiPaper: { styleOverrides: { root: { borderRadius: 12 } } },
    MuiTextField: { defaultProps: { variant: 'outlined', size: 'small' } },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          backgroundColor: '#f7f7f9',
          '& fieldset': { borderColor: '#e5e7eb' },
          '&:hover fieldset': { borderColor: '#cbd5e1' },
          '&.Mui-focused fieldset': { borderColor: '#94a3b8' },
        },
      },
    },
    MuiButton: {
      defaultProps: { variant: 'outlined' },
      styleOverrides: {
        root: { borderRadius: 12, textTransform: 'none', fontWeight: 600 },
        outlined: { backgroundColor: '#fff', borderColor: '#e5e7eb', '&:hover': { backgroundColor: '#f8fafc' } },
      },
    },
  },
});

export default theme;
export { theme };

