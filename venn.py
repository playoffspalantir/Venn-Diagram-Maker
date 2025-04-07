import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import matplotlib.font_manager as fm

def generate_venn(sets_text, set_labels, venn_type, colors, font_family, font_size, font_color, bold_labels):
    """Generates a custom Venn diagram with text labels in the regions.

    Args:
        sets_text: A tuple of strings, each being the text to place in a region.
        set_labels: A tuple of strings for the set labels (A, B, C).
        venn_type: "2" or "3" for the diagram type.
        colors: A tuple of colors for the circles.
        font_family: Font family for all text.
        font_size: Font size for all text.
        font_color: Font color for all text.
        bold_labels:  Boolean, whether the labels should be bold.
    """

    plt.figure(figsize=(8, 8))
    ax = plt.gca()  # Get the current axes object
    ax.set_axis_off()

    font_weight = 'bold' if bold_labels else 'normal'
    font_props = fm.FontProperties(family=font_family, size=font_size, weight=font_weight)

    if venn_type == "2":
        v = venn2(subsets=(1, 1, 1), set_labels=set_labels, set_colors=colors, ax=ax) # Dummy values for subsets
    elif venn_type == "3":
        v = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=set_labels, set_colors=colors, ax=ax) # Dummy values for subsets
    else:
        st.error("Invalid Venn type. Choose '2' or '3'.")
        return

    # Remove the default numbers
    if v is not None:
        for text in v.subset_labels:
            if text:
                text.set_visible(False)  # Hide the default labels

    if v is not None:
        for text in v.set_labels:
            if text:
                text.set_fontproperties(font_props)
                text.set_color(font_color)


    # Add custom text to the regions
    if venn_type == "2":
        centers = v.centers  # Get the centers of the circles
        if centers is not None:
            ax.text(centers[0].x - 0.15, centers[0].y, sets_text[0], ha='center', va='center', fontproperties=font_props, color=font_color) #A only
            ax.text(centers[1].x + 0.15, centers[1].y, sets_text[1], ha='center', va='center', fontproperties=font_props, color=font_color) #B only

        intersection_center = (centers[0].x + centers[1].x) / 2, (centers[0].y + centers[1].y) / 2
        ax.text(intersection_center[0], intersection_center[1], sets_text[2], ha='center', va='center', fontproperties=font_props, color=font_color) #A&B

    elif venn_type == "3":
        centers = v.centers
        if centers is not None:
            ax.text(centers[0].x - 0.25, centers[0].y + 0.05, sets_text[0], ha='center', va='center', fontproperties=font_props, color=font_color) #A only
            ax.text(centers[1].x + 0.25, centers[1].y + 0.05, sets_text[1], ha='center', va='center', fontproperties=font_props, color=font_color) #B only
            ax.text(centers[2].x, centers[2].y - 0.3, sets_text[2], ha='center', va='center', fontproperties=font_props, color=font_color) #C Only

        #Approximate Intersection Centers
        ax.text((centers[0].x + centers[1].x) / 2, (centers[0].y + centers[1].y) / 2 + 0.20, sets_text[3], ha='center', va='center', fontproperties=font_props, color=font_color) #AB
        ax.text((centers[0].x + centers[2].x) / 2 -0.20 , (centers[0].y + centers[2].y) / 2 - 0.1, sets_text[4], ha='center', va='center', fontproperties=font_props, color=font_color) #AC
        ax.text((centers[1].x + centers[2].x) / 2 +0.20, (centers[1].y + centers[2].y) / 2 - 0.1, sets_text[5], ha='center', va='center', fontproperties=font_props, color=font_color) #BC

        #Center Intersection
        ax.text(sum([c.x for c in centers])/len(centers),sum([c.y for c in centers])/len(centers), sets_text[6], ha='center', va='center', fontproperties=font_props, color=font_color) #ABC


    st.pyplot(plt)
    plt.close()


def main():
    st.title("Venn Diagram Generator")

    venn_type = st.radio("Venn Diagram Type:", ("2", "3"), horizontal=True)

    st.subheader("Text for Venn Diagram Regions:")
    if venn_type == "2":
        text_a_only = st.text_input("Text for Region A only:", "Text for A")
        text_b_only = st.text_input("Text for Region B only:", "Text for B")
        text_ab = st.text_input("Text for Region A and B:", "Text for A and B")
        sets_text = (text_a_only, text_b_only, text_ab)
    else:
        text_a_only = st.text_input("Text for Region A only:", "Text for A")
        text_b_only = st.text_input("Text for Region B only:", "Text for B")
        text_c_only = st.text_input("Text for Region C only:", "Text for C")
        text_ab = st.text_input("Text for Region A and B:", "Text for A and B")
        text_ac = st.text_input("Text for Region A and C:", "Text for A and C")
        text_bc = st.text_input("Text for Region B and C:", "Text for B and C")
        text_abc = st.text_input("Text for Region A, B, and C:", "Text for A, B, and C")
        sets_text = (text_a_only, text_b_only, text_c_only, text_ab, text_ac, text_bc, text_abc)

    st.subheader("Set Labels (A, B, C):")
    if venn_type == "2":
        label_a = st.text_input("Label for Set A:", "Set A")
        label_b = st.text_input("Label for Set B:", "Set B")
        set_labels = (label_a, label_b)

    else:
        label_a = st.text_input("Label for Set A:", "Set A")
        label_b = st.text_input("Label for Set B:", "Set B")
        label_c = st.text_input("Label for Set C:", "Set C")
        set_labels = (label_a, label_b, label_c)


    st.subheader("Colors")
    if venn_type == "2":
        color_a = st.color_picker("Color for Set A:", "#0072B2")
        color_b = st.color_picker("Color for Set B:", "#D55E00")
        colors = (color_a, color_b)
    else:
        color_a = st.color_picker("Color for Set A:", "#0072B2")
        color_b = st.color_picker("Color for Set B:", "#D55E00")
        color_c = st.color_picker("Color for Set C:", "#009E73")
        colors = (color_a, color_b, color_c)

    st.subheader("Font Styling")
    available_fonts = ['sans-serif', 'serif', 'monospace', 'Arial', 'Times New Roman']
    font_family = st.selectbox("Font Family:", options=available_fonts, index=0)
    font_size = st.slider("Font Size:", min_value=8, max_value=24, value=12)
    font_color = st.color_picker("Font Color:", "#000000")
    bold_labels = st.checkbox("Bold Labels", value=False)

    if st.button("Generate Diagram"):
        generate_venn(sets_text, set_labels, venn_type, colors, font_family, font_size, font_color, bold_labels)

if __name__ == "__main__":
    main()