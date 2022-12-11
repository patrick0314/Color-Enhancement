import numpy

class CIECAM02(object):
    """
    **References**

    * CIE TC 8-01 (2004). A Color appearance model for color management systems.
      Publication 159. Vienna: CIE Central Bureau. ISBN 3-901906-29-0.
    * Fairchild, M. D. (2013). *Color appearance models*, 3rd Ed. John Wiley & Sons.
    """

    @property
    def hue_angle(self): return self._h

    @property
    def chroma(self): return self._chroma

    @property
    def saturation(self): return self._saturation

    @property
    def lightness(self): return self._lightness

    @property
    def brightness(self): return self._brightness

    @property
    def colorfulness(self): return self._colorfulness

    @property
    def a(self): return self._a

    @property
    def b(self): return self._b

    @property
    def n(self): return self._n

    @property
    def et(self): return self.e_t

    @property
    def A(self): return self._A

    @property
    def nbb(self): return self.n_bb

    @property
    def Fl(self): return self.f_l

    M_CAT02 = numpy.array([[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]])
    M_CAT02_inv = numpy.linalg.inv(M_CAT02)
    M_HPE = numpy.array([[0.38971, 0.68898, -0.07868], [-0.22981, 1.18340, 0.04641], [0, 0, 1]])

    def __init__(self, x, y, z, x_w, y_w, z_w, y_b, l_a, c, n_c, f, d=False):
        """
        :param x: X value of test sample :math:`X`.
        :param y: Y value of test sample :math:`Y`.
        :param z: Z value of test sample :math:`Z`.
        :param x_w: X value of reference white :math:`X_W`.
        :param y_w: Y value of reference white :math:`Y_W`.
        :param z_w: Z value of reference white :math:`Z_W`.
        :param y_b: Background relative luminance :math:`Y_b`.
        :param l_a: Adapting luminance :math:`L_A` in cd/m^2.
        :param c: Exponential nonlinearity :math:`c`. (Average/Dim/Dark) (0.69/0.59/0.525).
        :param n_c: Chromatic induction factor :math:`N_c`. (Average/Dim/Dark) (1.0,0.9,0.8).
        :param f: Maximum degree of adaptation :math:`F`. (Average/Dim/Dark) (1.0/0.9/0.8).
        :param d: Discount-the-Illuminant factor :math:`D`.
        """

        xyz = numpy.array([x, y, z])
        xyz_w = numpy.array([x_w, y_w, z_w])

        # Determine the degree of adaptation
        if not d: d = self._compute_degree_of_adaptation(f, l_a)
        else: d = 1

        # Compute viewing condition dependant components
        k = 1 / (5 * l_a + 1)

        self.f_l = 0.2 * (k ** 4) * 5 * l_a + 0.1 * (1 - k ** 4) ** 2 * (5 * l_a) ** (1 / 3)
        self._n = y_b / y_w
        self.n_bb = self.n_cb = 0.725 * self._n ** -0.2
        z = 1.48 + numpy.sqrt(self._n)

        rgb_a, rgb_aw = self._compute_adaptation(xyz, xyz_w, self.f_l, d)

        r_a, g_a, b_a = rgb_a
        r_aw, g_aw, b_aw = rgb_aw

        # Opponent Color Dimensions
        self._a = r_a - 12 * g_a / 11 + b_a / 11
        self._b = (1 / 9) * (r_a + g_a - 2 * b_a)

        # Hue
        self._h = 360 * numpy.arctan2(self._b, self._a) / (2 * numpy.pi)
        self.e_t = (1 / 4) * (numpy.cos(2 + self._h * numpy.pi / 180) + 3.8)

        # Lightness
        self._A = self._compute_achromatic_response(r_a, g_a, b_a, self.n_bb)
        a_w = self._compute_achromatic_response(r_aw, g_aw, b_aw, self.n_bb)
        self._lightness = 100 * (self._A / a_w) ** (c * z)  # 16.24

        # Brightness
        # self._brightness = self.compute_brightness(self.lightness, surround, a_w, f_l)
        self._brightness = (4 / c) * numpy.sqrt(self._lightness / 100) * (a_w + 4) * self.f_l ** 0.25

        # Chroma
        # self.chroma = self.compute_chroma(rgb_a, self.lightness, surround, self.N_cb, e_t, self.a, self.b, n)
        t = ((50000 / 13) * n_c * self.n_cb * self.e_t * numpy.sqrt((self._a ** 2) + (self._b ** 2))) / (
            rgb_a[0] + rgb_a[1] + (21 / 20) * rgb_a[2])
        self._chroma = (t ** 0.9) * numpy.sqrt(self._lightness / 100) * ((1.64 - 0.29 ** self._n) ** 0.73)

        # Colorfulness
        self._colorfulness = self.chroma * self.f_l ** 0.25

        # Saturation
        self._saturation = 100 * numpy.sqrt(self._colorfulness / self._brightness)

        # Cartesian coordinates
        self.a_c, self.b_c = self._compute_cartesian_coordinates(self.chroma, self._h)
        self.a_m, self.b_m = self._compute_cartesian_coordinates(self._colorfulness, self._h)
        self.a_s, self.b_s = self._compute_cartesian_coordinates(self.saturation, self._h)

    @classmethod
    def _compute_adaptation(cls, xyz, xyz_w, f_l, d):
        # Transform input colors to cone responses
        rgb = cls._xyz_to_rgb(xyz)
        rgb_w = cls._xyz_to_rgb(xyz_w)

        # Compute adapted tristimulus-responses
        rgb_c = cls._white_adaption(rgb, rgb_w, d)
        rgb_cw = cls._white_adaption(rgb_w, rgb_w, d)

        # Convert adapted tristimulus-responses to Hunt-Pointer-Estevez fundamentals
        rgb_p = cls._compute_hunt_pointer_estevez_fundamentals(rgb_c)
        rgb_wp = cls._compute_hunt_pointer_estevez_fundamentals(rgb_cw)

        # Compute post-adaptation non-linearities
        rgb_ap = cls._compute_nonlinearities(f_l, rgb_p)
        rgb_awp = cls._compute_nonlinearities(f_l, rgb_wp)

        return rgb_ap, rgb_awp

    @staticmethod
    def _xyz_to_rgb(xyz):
        return numpy.dot(CIECAM02.M_CAT02, xyz)

    @staticmethod
    def _rgb_to_xyz(rgb):
        return numpy.dot(CIECAM02.M_CAT02_inv, rgb)

    @staticmethod
    def _white_adaption(rgb, rgb_w, d=1):
        return ((100 * d / rgb_w) + (1 - d)) * rgb

    @staticmethod
    def _compute_degree_of_adaptation(surround_conditions, adapting_luminance):
        return surround_conditions * (1 - (1 / 3.6) * numpy.exp((-adapting_luminance - 42) / 92))

    @staticmethod
    def _compute_hunt_pointer_estevez_fundamentals(rgb):
        return numpy.dot(numpy.dot(CIECAM02.M_HPE, CIECAM02.M_CAT02_inv), rgb)

    @staticmethod
    def _compute_nonlinearities(f_l, rgb):
        return 0.1 + (400 * (f_l * rgb / 100) ** 0.42) / (27.13 + (f_l * rgb / 100) ** 0.42)

    @staticmethod
    def _compute_achromatic_response(r, g, b, n_bb):
        return (2 * r + g + (1 / 20) * b - 0.305) * n_bb

    @staticmethod
    def _compute_cartesian_coordinates(value, hue):
        a = value * numpy.cos(hue * numpy.pi / 180)  # 16.30
        b = value * numpy.sin(hue * numpy.pi / 180)  # 16.31
        return a, b
