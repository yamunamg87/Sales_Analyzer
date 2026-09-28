import streamlit as st

st.title('welcome to streamlit')

# inputs

m1= st.text_input('enter your input')
st.markdown(m1)

m2 =st.text_area('enter your input')
st.markdown(m2)

st.warning('please enter your input')

st.success('updated successfully')

m3 = st.selectbox('please select',{'python','java','sql'})
st.markdown(m3)

m4 = st.multiselect('please select',{'python','java','sql'})
st.markdown(m4)

st.radio('please select',{'python','java','sql'})

st.sidebar.text_input('Enter your name')
st.sidebar.selectbox('please select',{'python','java','SQL'})
st.sidebar.radio('please select',{'python','java','SQL'})



